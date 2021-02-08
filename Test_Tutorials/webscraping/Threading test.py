from concurrent.futures import ThreadPoolExecutor
from time import sleep
import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.bermudayp.com/businesses/search/'
urls = [f'{url}{page}/construction' for page in range(1, 20 + 1) ]


def grep_id(url):
        print('page start')
        # load webpage content
        r = requests.get(url)

        soup = bs(r.content, features='html.parser')

        business_collect = soup.select('div[data-listing-id]')
        for id in business_collect:
            return int(id['data-listing-id'])


def task(message):
    sleep(2)
    return message


def main():
    executor = ThreadPoolExecutor(5)
    future = executor.submit(grep_id, urls)
    print(future.done())
    sleep(2)
    print(future.done())
    print(future.result())


if __name__ == '__main__':
    main()