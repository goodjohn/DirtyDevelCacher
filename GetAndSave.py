#!/usr/bin/python3.4

from urllib.request import urlopen
from pprint import pprint

example_site = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'
example_pic  = 'http://books.toscrape.com/media/cache/da/a0/daa08c54a927c27494ea5bb90af79c60.jpg'

page = urlopen(example_site)

pprint(page.status)
pprint(dict(page.info()))

print()

pic = urlopen(example_pic)

pprint(pic.status)
pprint(dict(pic.info()))

print()
