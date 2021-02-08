import requests
from bs4 import BeautifulSoup as bs
import concurrent.futures
import threading
import time

"""
Documentation website
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

"""
"""
 
 MAIN CONTENT CLASS  
 class = main-info col-sm-4
    BUSINESS NAME
        class = 'block-title'
    ADDRESS
        itemprop="address"
    NUMBER
        class="box-ico phone-i"
 
 EXTRAS
 class = description
 class = main-tags (wrapped in href)
 class = secondary-tags (wrapped in href)

"""

class BusinessSearch:
    def __init__(self, category):
        self.search_page = 'https://www.bermudayp.com/businesses/search/'
        self.category = category
        print(f'Running {self.category.capitalize()} Search')

        self.business_ids = []
        self.hits = 0
        self.pages = 0
        self.setup()

    def setup(self):
        self.hit_search()
        self.grab_business_ids()

    def hit_search(self):

        url = f'{self.search_page}1/{self.category}'
        # load webpage content
        r = requests.get(url)
        soup = bs(r.content, features='html.parser')
        self.hits = int(soup.find('div', attrs={'class': 'results'}).span.string)
        self.page_count(self.hits)

    def page_count(self, hits):
        '''
        Input Hits
        :param hits:
        :return:
        '''
        self.pages = hits/10
        if not self.pages.is_integer():
            self.pages = int(self.pages) + 1

    def grab_business_ids(self):
        def get_ids(content):
            soup = bs(content, features='html.parser')
            business_collect = soup.select('div[data-listing-id]')
            for id in business_collect:
                self.business_ids.append(int(id['data-listing-id']))

        def get_session():
            if not hasattr(thread_local, "session"):
                thread_local.session = requests.Session()
            return thread_local.session

        def download_site(url):
            session = get_session()
            with session.get(url) as response:
                # print(f"Read {round((len(response.content)/1024)/2)} mb from {url}")
                get_ids(response.content)

        def download_all_sites(sites):
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.pages) as executor:
                executor.map(download_site, sites)

        thread_local = threading.local()
        sites = [f'{self.search_page}{page}/construction' for page in range(1, self.pages + 1)]
        start_time = time.time()
        download_all_sites(sites)
        duration = time.time() - start_time
        print(f"Downloaded {len(sites)} pages of {self.category.capitalize()} in {duration} seconds")


if __name__ == '__main__':

    construction = BusinessSearch('construction')
    cars = BusinessSearch('cars')
    newlist = []
    newlist = construction.business_ids + cars.business_ids
    print(len(construction.business_ids))
    print(len(cars.business_ids))

    print(len(newlist))