#!/usr/bin/python3.4

import urllib
from urllib.request import urlopen
from pprint import pprint

urls = {
    'example_site': 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html',
    'example_pic': 'http://books.toscrape.com/media/cache/da/a0/daa08c54a927c27494ea5bb90af79c60.jpg',
    'example_404': 'http://books.toscrape.com/this-url-doesnt-exist',
    'example_403': 'http://books.toscrape.com/media/'
}

for desc, url in urls.items():
    print()
    print(desc)
    print(url)
    try:
        response = urlopen(url)
        pprint('Response Code: {}'.format(response.status))
        pprint(dict(response.info()))
    except urllib.error.HTTPError as e:
        pprint('Failed: {}'.format(e))
    print()
