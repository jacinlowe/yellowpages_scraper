import concurrent.futures
import math
import threading

import requests

from initial_id_grab import BusinessSearch
from runtime_decorator import timeit
from scrape_code import get_ids as grab_data


@timeit
def get_data_concurrent(sites, max_workers=20):
    temp_id = []

    def get_ids(content, category):
        id_grab = grab_data(content, category)

        temp_id.append(id_grab)

    def get_session():
        if not hasattr(thread_local, "session"):
            thread_local.session = requests.Session()
        return thread_local.session

    def download_site(payload):
        session = get_session()
        single_url = payload[1]
        catagory = payload[0]
        with session.get(single_url) as response:
            # print(f"Read {round((len(response.content)/1024)/2)} mb from {url}")
            get_ids(response, catagory)

    def download_all_sites(websites, trs: int):
        with concurrent.futures.ThreadPoolExecutor(max_workers=trs) as executor:
            executor.map(download_site, websites)

    download_all_sites(sites, max_workers)

    return temp_id


# Pass in max workers based off ids / some number
# Pass in the catagories

thread_local = threading.local()
url = 'https://www.bermudayp.com/listing/view/'
categories = ['mechanic', 'construction']
ids = []
site_payload = []
for cats in categories:
    blist = BusinessSearch(cats).business_ids
    # ids = ids + blist
    site = [f'{url}{str(site)}' for site in blist]
    ids = ids + [[cats, i] for i in site]
    site_payload = ids

num_id = len(ids)
print(f'{num_id} IDs Collected')
# print(site_payload)

# sites = [f'{url}{str(site[1])}' for site in ids]
# list_of_businesses = []

# ID length Check
if num_id >= 50:
    work_threads = math.sqrt(num_id) * 3
else:
    work_threads = num_id

print(f'Running info grab')

list_of_businesses = get_data_concurrent(site_payload, work_threads)
print(f'{len(list_of_businesses)} business content grabbed')
print(list_of_businesses[:3])
