#!/usr/bin/python3.4

from urllib.request import urlopen

example_site = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'

print(urlopen(example_site).read().decode())

