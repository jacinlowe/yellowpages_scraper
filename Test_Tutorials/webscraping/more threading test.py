from bs4 import BeautifulSoup as bs
 ## THREADING
import concurrent.futures
import requests
import threading
import time

import openpyxl


# def get_ids(content):
#
#     # ### BUSINESS NAME ###
#     soup = bs(content, features='html.parser')
#     title = soup.find(attrs={'class': 'block-title'}).h3.string
#
#     ### ADDRESS ####
#     address = soup.find_all('span', attrs={'itemprop': [
#         'streetAddress',
#         'postOfficeBoxNumber',
#         'addressRegion',
#         'addressCountry',
#         'postalCode'
#
#     ]})
#     address = [text.get_text() for text in address]
#
#     # ### PHONE NUMBER ###
#     phone_number = soup.find_all(attrs={'class': 'box-ico phone-i'})
#
#     phone_number = [call.a.get('href')[4:] for call in phone_number]
#
#     # ### DESCRIPTION ###
#     description = soup.find(attrs={'class': 'description'})
#     description = description.find_all('p')
#     description = [d.get_text() for d in description]
#
#     # ### TAGS ###
#     tags = soup.find_all(attrs={'class': ("main-tags", 'secondary-tags')})
#     tags = [b.get_text() for i in tags for b in i.find_all('a')]
#
#     # ### LOGO ###
#     logo = soup.find(attrs={'class': 'logo'}).get('src')
#
#     business = {'Name'         : title,
#                 'Address'      : address,
#                 'Phone Numbers': phone_number,
#                 'Description'  : description,
#                 'Tags'         : tags,
#                 'Logo'         : logo
#                 }
#     businesses.append(business)
#
# def get_session():
#     if not hasattr(thread_local, "session"):
#         thread_local.session = requests.Session()
#     return thread_local.session
#
#
# def download_site(url):
#     session = get_session()
#     with session.get(url) as response:
#         # print(f"Read {round((len(response.content)/1024)/2)} mb from {url}")
#         get_ids(response.content)
#
#
# def download_all_sites(sites):
#     # ### ADD 10 more workers than needed seems the sweet spot
#     with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
#         executor.map(download_site, sites)
#
#
# def save_excel_book(workbook):
#     workbook.save('file.xlsx')
#
#
# def store_to_database(b_list):
#     wb = openpyxl.Workbook()
#     ws = wb.active
#     headers = ['Name', 'Address', 'Phone Numbers', 'Description', 'Tags', 'Logo']
#     ws.append(headers)
#     for line in b_list:
#         # create generator to yield product value
#         # use headers in desired order as `key`
#         values = (line[k] for k in headers)
#         l = []
#         for v in values:
#             if isinstance(v, list):
#                 collected = ', '.join(v)
#                 l.append(collected)
#             else:
#                 l.append(v)
#         ws.append(l)
#     save_excel_book(wb)
#

def scrape_content():
    def get_ids(content):

        # ### BUSINESS NAME ###
        soup = bs(content, features='html.parser')
        title = soup.find(attrs={'class': 'block-title'}).h3.string

        ### ADDRESS ####
        address = soup.find_all('span', attrs={'itemprop': [
            'streetAddress',
            'postOfficeBoxNumber',
            'addressRegion',
            'addressCountry',
            'postalCode'

        ]})
        address = [text.get_text() for text in address]

        # ### PHONE NUMBER ###
        phone_number = soup.find_all(attrs={'class': 'box-ico phone-i'})

        phone_number = [call.a.get('href')[4:] for call in phone_number]

        # ### DESCRIPTION ###
        description = soup.find(attrs={'class': 'description'})
        description = description.find_all('p')
        description = [d.get_text() for d in description]

        # ### TAGS ###
        tags = soup.find_all(attrs={'class': ("main-tags", 'secondary-tags')})
        tags = [b.get_text() for i in tags for b in i.find_all('a')]

        # ### LOGO ###
        logo = soup.find(attrs={'class': 'logo'}).get('src')

        business = {'Name'         : title,
                    'Address'      : address,
                    'Phone Numbers': phone_number,
                    'Description'  : description,
                    'Tags'         : tags,
                    'Logo'         : logo
                    }
        list_of_businesses.append(business)
        print(len(list_of_businesses))

    def get_session():
        if not hasattr(thread_local, "session"):
            thread_local.session = requests.Session()
        return thread_local.session

    def download_site(url):
        session = get_session()
        with session.get(url) as response:
            print(f"Read {round((len(response.content)/1024)/2)} mb from {url}")
            get_ids(response.content)

    def download_all_sites(sites):
        # ### ADD 10 more workers than needed seems the sweet spot
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            executor.map(download_site, sites)

    def save_excel_book(workbook):
        workbook.save('file.xlsx')

    def store_to_database(b_list):
        wb = openpyxl.Workbook()
        ws = wb.active
        headers = ['Name', 'Address', 'Phone Numbers', 'Description', 'Tags', 'Logo']
        ws.append(headers)
        for line in b_list:
            # create generator to yield product value
            # use headers in desired order as `key`
            values = (line[k] for k in headers)
            l = []
            for v in values:
                if isinstance(v, list):
                    collected = ', '.join(v)
                    l.append(collected)
                else:
                    l.append(v)
            ws.append(l)
        save_excel_book(wb)

    global thread_local
    global list_of_businesses



    thread_local = threading.local()
    list_of_businesses = []

    url = 'https://www.bermudayp.com/listing/view/'
    ids = [32553, 32652, 32628, 32893, 33035, 33163, 33234, 33504,
            35022, 58525, 31932, 32293, 32346, 32402, 32956, 33369,
            35087, 35326, 58487, 58490, 84578, 58567, 98543, 180585,
            427727, 433163, 433305, 482582, 32726, 38247, 135547, 480760,
            481626, 140729, 29706, 31838, 432803, 30494, 180680, 481751,
            480745, 30291, 30416, 30422, 30769, 31317, 31319, 31400, 31654,
            31819, 32480, 31618, 432274, 31820, 31710, 33008, 33829, 58557,
            98558, 180610, 180691, 480694, 110683, 31459, 181028, 398464,
            458153, 458372, 482368, 32173, 31658, 31652, 31945, 33208, 481532,
            29568, 30470, 32709, 32712, 32899, 32992, 33060, 33392, 33402, 31226,
            433145, 30682, 30480, 33880, 31667, 433152, 180756, 465401, 33890,
            33455, 38319, 84534, 98762, 180419, 433037, 411254, 29414, 29524,
            29594, 30599, 31973, 32725, 35021, 433685, 118697, 31589, 58556,
            35219, 33751, 29965, 30134, 482015, 29900, 30408, 30446,
            30705, 30793, 31061, 31698, 30286, 30273, 30351, 30417,
            31262, 31348, 31343, 31454, 31495, 31616, 33288, 35233, 32502,
            33336, 32519, 453809, 482010, 29383, 29762, 30668, 33505, 31303,
            29548, 30423, 30717, 31681, 38194, 29299, 31640, 32546, 180534,
            30893, 33058, 32331, 482513, 29311, 30883, 481836, 29491, 38279,
            30913, 433059, 480754, 32587, 29710, 180679, 33798, 481877, 481106,
            31822, 180536, 32234, 30687, 180535, 180538, 30914, 31325, 180537,
            31816, 31471, 33084, 33334, 38254, 38320, 31846, 31939, 33556, 32721,
            32647, 33171
           ]
    id_total = []
    # , 180534, 481836, 482513, 30883, 33058, 29311, 32331,
    # Change the URL and IDs for classes
    # if len(ids) >= 99:
    #     id1 = ids[:99]
    #     id2 = ids[99:]
    #     id_total.append(id1)
    #     id_total.append(id2)
    # print(id_total)
    sites = [f'{url}{str(site)}' for site in ids[99:]]
    
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded content of {len(sites)} sites in {duration} seconds")
    print(len(list_of_businesses))
    # store_to_database(list_of_businesses)


if __name__ == "__main__":
    scrape_content()

    # print(businesses)





# ### MULTI PROCESSING ###
# import requests
# import multiprocessing
# import time
#
# session = None
#
#
# def set_global_session():
#     global session
#     if not session:
#         session = requests.Session()
#
#
# def download_site(url):
#     with session.get(url) as response:
#         name = multiprocessing.current_process().name
#         print(f"{name}:Read {len(response.content)} from {url}")
#
#
# def download_all_sites(sites):
#     with multiprocessing.Pool(initializer=set_global_session) as pool:
#         pool.map(download_site, sites)
#
#
# if __name__ == "__main__":
#     url = 'https://www.bermudayp.com/businesses/search/'
#     sites = [f'{url}{page}/construction' for page in range(1, 20 + 1)]
#     start_time = time.time()
#     download_all_sites(sites)
#     duration = time.time() - start_time
#     print(f"Downloaded {len(sites)} in {duration} seconds")


# # ### NORMAL RUN ###
# def download_site(url):
#     session = requests.session()
#     with session.get(url) as response:
#         print(f"Read {len(response.content)} from {url}")
#
#
# def grab_business_ids(pages):
#     for page in pages:
#         download_site(page)
#
#
# if __name__ == '__main__':
#     url = 'https://www.bermudayp.com/businesses/search/'
#     sites = [f'{url}{page}/construction' for page in range(1, 20 + 1)]
#     #  Timer
#     start_time = time.time()
#     grab_business_ids(sites)
#     duration = time.time() - start_time
#     print(f"Downloaded {len(sites)} in {duration} seconds")

"""
    multi threading:        2.79
                            2.77 
    asyncio:                1.68 
                            1.67
    threading(50 workers):  1.95
                            1.74
                            
    normal:                 14.4
                            17.3
"""