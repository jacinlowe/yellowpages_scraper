import time

import pyrebase
import requests

from initial_id_grab import BusinessSearch
from scrape_code import get_ids

"""
Pyrebase instructions
https://github.com/thisbejim/Pyrebase
"""

config = {
    'apiKey'       : 'apiKey',
    'authDomain'   : 'fir-test-c7bf2-default-rtdb.firebaseio.com',
    'databaseURL'  : 'https://fir-test-c7bf2-default-rtdb.firebaseio.com/',
    'storageBucket': 'projectId.appspot.com'
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()


def main():
    url = 'https://www.bermudayp.com/listing/view/'
    categories = ['mechanic']
    ids = []
    for cats in categories:
        ids = ids + BusinessSearch(cats).business_ids
    print(f'{len(ids)} IDs Collected')
    # print(ids)
    sites = [f'{url}{str(site)}' for site in ids]
    list_of_businesses = []
    print(f'Running info grab')
    count = 0
    start_time = time.time()
    for site in sites:
        #     # print(site)
        r = requests.get(site)
        # id_grab = get_ids(r)
        #     db.child('Businesses').push(id_grab)
        list_of_businesses.append(get_ids(r))
        count += 1
        print(count)

    duration = time.time() - start_time
    print(f"Grabbed {len(list_of_businesses)} Businesses info in {duration} seconds")
    # wb = 'newfile.xlsx'
    # wb = open_workbook(wb)
    # store_to_database(list_of_businesses, wb)
    # save_excel_book(wb)
    # wb.save('temp.xlsx')


if __name__ == '__main__':
    main()