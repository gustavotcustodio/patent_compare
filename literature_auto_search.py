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
import numpy as np

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
                                for _ in range(n_results)]
        # time.sleep(1)
        # for _ in range(n_results):
        #     res = next(generator_results).fill()
        #     time.sleep(1)
        #     self.results_scholar.append(res)
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

    def plot_hist_article(self, x, info, n_bins=None):
        """ Plot an histogram with the frequency of the variable x."""
        if n_bins:
            plt.hist(x, bins=n_bins)
        else:
            plt.hist(x)
        plt.title('Artigos mais relevantes por {}'.format(info))
        plt.xlabel(info.capitalize())
        plt.ylabel('Quantidade')
        plt.show()

    def get_bib_info(self, publications, info):
        # Check if publication contains the info, if it doesn't search for it.
        n_publications = len(publications)
        info_articles = []
        for i in range(n_publications):
            if info in publications[i].bib:
                info_articles.append(publications[i].bib[info])
            else:
                publications[i] = publications[i].fill()
                info_articles.append(publications[i].bib[info])
        return info_articles

    def get_n_citations(self, publications):
        return list(map(lambda pub: pub.citedby, publications))


def main():
    searcher = LiteratureAutoSearch()
    query = input('Digite o nome da patente para ser buscada: ')
    n_results = int(input('Digite o número de artigos mais'+
                        ' relevantes para serem recuperados: '))
    publications = searcher.search_scholar(query, n_results)

    n_citations = searcher.get_n_citations(publications)
    #years = searcher.get_bib_info(publications, 'year')

    #print(publications[2].bib['year'])
    searcher.plot_hist_article(n_citations, 'número de citações')
    #searcher.plot_hist_article(years, 'year')

if __name__ == '__main__':
    main()
