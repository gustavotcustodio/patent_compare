import os
import re
import scholarly
import itertools
import pypatent
import urllib.request
import json
from collections import Counter
import time
from matplotlib import pyplot as plt

class LiteratureAutoSearch():
    def __init__(self):
        self.results_scholar = []
        self.results_patents = []

    def search_scholar(self, query, n_results):
        """ Returns a list containing the n_results most relevant
        Publications to the keywords.

        Parameters
        ----------
        query: string
            Query to search on Google Scholar.
        n_results: int
            Number of articles to return.

        Returns
        -------
        results: list(Publications)
            List containing Publication objects.
        """
        generator_results = scholarly.search_pubs_query(query)
        self.results_scholar = [next(generator_results)
                                for _ in range(2)]
        time.sleep(1)
        for _ in range(n_results):
            res = next(generator_results).fill()
            time.sleep(1)
            self.results_scholar.append(res)
        return self.results_scholar

    def search_patent(self, patent_title, n_patents):
        """ Returns a list containing the n_patents most relevant
        patents according to the title.

        Parameters
        ----------
        patent_title: string
            Keyword to search on Google Patents.
        n_patents: int
            Number of patents to return.

        Returns
        -------
        results: list(dict)
            List containing a dictionatry for the relevant patents.
        """
        search_results = pypatent.Search(patent_title,
                                        get_patent_details=False,
                                        results_limit=n_patents).as_list()
        return search_results

    def plot_info_by_year(self, dict_year_count):
        return None

    def get_year_and_count(self, publications):
        years = list(map(lambda pub: pub.bib['year'], publications))
        count = dict(Counter(years))
        return count

    def plot_info_by_year(dict_year):
        return None
        #plt.bar()


def main():
    searcher = LiteratureAutoSearch()
    results = searcher.search_scholar('python', 4)
    print(results[0].bib['title'])


if __name__ == '__main__':
    main()
