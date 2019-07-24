import unittest
import numpy as np
import datetime
from literature_auto_search import LiteratureAutoSearch
from scholarly import Publication
from unittest.mock import patch

class TestLiteratureAutoSearch(unittest.TestCase):
    def setUp(self):
        self.searcher = LiteratureAutoSearch()
        self.publications = []
        self.titles  = ['Title scholar no accent', 
                        'Tírulo com acento',
                        'Teste 3',
                        'Teste 4',
                        'Teste 5']
        self.years = [2017, 2005, 1998, 2017, 2019]
        self.citedby = [100, 0, 1, 20, 1000]
        for i in range(5):
            self.publications.append(Publication('a'))
            self.publications[i].bib['title'] = self.titles[i]
            self.publications[i].citedby = self.citedby[i]
            self.publications[i].bib['year'] = self.years[i]

    @unittest.skip("too slow")
    def test_search_scholar(self):
        query = '(algorithm OR software)("one camera" OR "single camera")'
        results = self.searcher.search_scholar(query, 5)
        self.assertEqual(results[1].bib['title'].strip(), 
            'MonoSLAM: Real-time single camera SLAM')
        self.assertEqual(results[2].bib['title'].strip(), 
            '3d gaze estimation with a single camera without ir illumination')

    @unittest.skip("problem fofr future")
    def test_search_patent(self):
        pat_title = 'PROCESSO DE OBTENÇÃO DE ÁCIDO ACÉTICO A PARTIR DE ETANOL'
        patent_info = self.searcher.search_patent(pat_title, 5)
        self.assertEqual(patent_info[0]['patent_num'], 'WO2013053032A1')

    def test_year_most_relevant(self):
        next_year = datetime.datetime.now().year + 1
        query = 'python'
        
        year_and_count = self.searcher.get_year_and_count(self.publications)
        print(year_and_count)
        # No patent can be from next year
        array_upper_bound = np.asarray(len(year_and_count)*[next_year])

        np.testing.assert_array_less(list(year_and_count.keys()), array_upper_bound)
        np.testing.assert_array_less(len(year_and_count)*[0], 
                                    list(year_and_count.values()))

    def test_plot_info_by_year(self):
        dict_year_count = {2010: 100, 2011: 50, 2012:1, 2013: 5}
        plot_info, = self.searcher.plot_info_by_year(dict_year_count)
        x_plot, y_plot = plot_info.get_xydata().T
        np.testing.assert_equal(x_plot, list(dict_year_count.keys()))

if __name__ == '__main__':
    unittest.main()