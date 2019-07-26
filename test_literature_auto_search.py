import unittest
import numpy as np
import datetime
import literature_auto_search
from scholarly import Publication
from unittest import mock

class TestLiteratureAutoSearch(unittest.TestCase):
    def setUp(self):
        self.searcher = literature_auto_search.LiteratureAutoSearch()
        self.publications = []
        self.titles  = ['Title scholar no accent', 
                        'Título com acento',
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

    #@unittest.skip("too slow")
    def test_search_scholar(self):
        query = '(algorithm OR software)("one camera" OR "single camera")'
        results = self.searcher.search_scholar(query, 5)
        for res in results:
            self.assertIsInstance(res, Publication)

    @unittest.skip("problem for future")
    def test_search_patent(self):
        pat_title = 'PROCESSO DE OBTENÇÃO DE ÁCIDO ACÉTICO A PARTIR DE ETANOL'
        patent_info = self.searcher.search_patent(pat_title, 5)
        self.assertEqual(patent_info[0]['patent_num'], 'WO2013053032A1')

    def test_get_bib_info(self):
        next_year = datetime.datetime.now().year + 1        
        years = self.searcher.get_bib_info(self.publications, 'year')
        # No patent can be from next year
        array_upper_bound = np.asarray(len(years)*[next_year])
        np.testing.assert_array_less(years, array_upper_bound)

    @mock.patch("%s.literature_auto_search.plt" % __name__)
    def test_plot_hist_article(self, mock_plt):
        years = [2010]*100 + [2011]*50 + [2012] + [2013]*5
        self.searcher.plot_hist_article(years, 'ano')
        assert(mock_plt.hist.called)
        assert(mock_plt.ylabel.called)
        assert(mock_plt.show.called)

    @mock.patch("%s.literature_auto_search.plt" % __name__)
    def test_plot_hist_article_n_bins(self, mock_plt):
        years = np.random.randint(1900, 2019, 300)
        self.searcher.plot_hist_article(years, 'ano', n_bins=10)
        assert(mock_plt.hist.called)
        assert(mock_plt.ylabel.called)
        assert(mock_plt.show.called)

if __name__ == '__main__':
    unittest.main()