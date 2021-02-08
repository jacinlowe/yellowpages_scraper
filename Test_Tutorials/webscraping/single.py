import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import threading
import requests
import openpyxl
import time


from Test_Tutorials.webscraping.scrape_code import get_ids, store_to_database, save_excel_book, open_workbook
from Test_Tutorials.webscraping.webscrapingtest import BusinessSearch

def main():
    url = 'https://www.bermudayp.com/listing/view/'
    categories = ['construction', 'cars']
    ids = []
    for cats in categories:
        ids = ids + BusinessSearch(cats).business_ids
    print(f'{len(ids)} IDs Collected')
    sites = [f'{url}{str(site)}' for site in ids]
    list_of_businesses = []
    print(f'Running info grab')
    count = 0
    start_time = time.time()
    for site in sites:
        # print(site)
        r = requests.get(site)
        list_of_businesses.append(get_ids(r))
        count += 1
        print(count)

    duration = time.time() - start_time
    print(f"Grabbed {len(list_of_businesses)} Businesses info in {duration} seconds")
    wb = 'newfile.xlsx'
    wb = open_workbook(wb)
    store_to_database(list_of_businesses, wb)
    # save_excel_book(wb)
    wb.save('BusinessList.xlsx')


if __name__ == '__main__':
    main()