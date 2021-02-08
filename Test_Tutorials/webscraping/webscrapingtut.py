import requests
from bs4 import BeautifulSoup as bs

"""
Documentation website
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

"""
# load the webpage content
r = requests.get("https://keithgalli.github.io/web-scraping/example.html")

#  Convert to a beautuful soup object
soup = bs(r.content, features="html.parser")

# print(soup.prettify())


# finds the first instance of the argument passed
first_header = soup.find('h2')


#  finds all the instances on the page of the argument passed
headers = soup.find_all("h2")


#  you can pass in list as well
first_header = soup.find(['h1', 'h2'])


headers = soup.find_all(['h1', 'h2'])


#  you can pass in attributes to the find/find_all function
paragraph = soup.find_all('p', attrs={'id': "paragraph-id"})

#  you can nest find/find_all calls
body = soup.find('body')
div = body.find('div')
header = div.find('h1')

#  we can search for specific strings in our find/find_all calls
# usefull when combined with the regex library

import re

string_search = soup.find_all('p', string=re.compile('Some'))

headers = soup.find_all('h2', string= re.compile('(H|h)eader'))


# select (CSS Selector)
#  https://www.w3schools.com/cssref/css_selectors.asp
content = soup.select('div p')
paragraphs = soup.select('h2 ~ p')

bold_text = soup.select('p#paragraph-id b')

paragraphs = soup.select('body > p')

#  grab element by specific property
#  soup.select('[align=middle]')
# print(paragraphs)

for paragraph in paragraphs:
    paragraph # print(paragraph.select('i'))

# get different properties of the HTML
# .string will grab only the content within that found element
header = soup.find('h2')

# print(header.string)

#  if multiple child elements use get_text
div = soup.find('div')
# print(div.prettify())

# print(div.get_text)

# get a specific property from an element
link = soup.find('a')
link = link['href']
# print(link)

paragraphs = soup.select('p#paragraph-id')
# print(paragraphs[0]['id'])

#path syntax
# parent, sibling, child
print(soup.body.prettify())