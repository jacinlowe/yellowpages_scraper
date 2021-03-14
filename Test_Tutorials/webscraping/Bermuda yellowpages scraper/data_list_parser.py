import concurrent.futures
import threading

import requests

from initial_id_grab import BusinessSearch
from runtime_decorator import timeit
from scrape_code import get_ids as grab_data


@timeit
def get_data_cocurrent(sites, max_workers=20):
    temp_id = []

    def get_ids(content):
        id_grab = grab_data(content)

        temp_id.append(id_grab)

    def get_session():
        if not hasattr(thread_local, "session"):
            thread_local.session = requests.Session()
        return thread_local.session

    def download_site(url):
        session = get_session()

        with session.get(url) as response:
            # print(f"Read {round((len(response.content)/1024)/2)} mb from {url}")
            get_ids(response)

    def download_all_sites(sites, trs: int):
        with concurrent.futures.ThreadPoolExecutor(max_workers=trs) as executor:
            executor.map(download_site, sites)

    download_all_sites(sites, max_workers)

    return temp_id


# Pass in max workers based off ids / some number
# Pass in the catagories

thread_local = threading.local()
url = 'https://www.bermudayp.com/listing/view/'
categories = ['mechanic']
ids = []
for cats in categories:
    ids = ids + BusinessSearch(cats).business_ids
print(f'{len(ids)} IDs Collected')
# print(ids)
sites = [f'{url}{str(site)}' for site in ids]
list_of_businesses = []

# print(sites[0])


print(f'Running info grab')

list_of_businesses = get_data_cocurrent(sites)
print(list_of_businesses[:3])
