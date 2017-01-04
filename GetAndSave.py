#!/usr/bin/python3.4

import urllib
from urllib.request import urlopen
from pprint import pprint
import json
import os
from hashlib import md5

urls = {
    'example_site': 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html',
    'example_pic': 'http://books.toscrape.com/media/cache/da/a0/daa08c54a927c27494ea5bb90af79c60.jpg',
    'example_404': 'http://books.toscrape.com/this-url-doesnt-exist',
    'example_403': 'http://books.toscrape.com/media/',
    'bad_url':  'http://books.to_scrape.com'
}

d = 'cache_files'

if not os.path.exists(d):
    os.makedirs(d)

for url in urls.values():
    url_header = {}
    try:
        response = urlopen(url)
        url_header = dict(response.info())
        url_header['net_conn'] = True
        url_header['status'] = response.status
    except urllib.error.HTTPError as e:
        url_header['net_conn'] = True
        url_header['status'] = e.status
    except urllib.error.URLError as e:
        url_header['net_conn'] = False
        url_header['reason'] = '{}'.format(e.reason)
    # fn = hash(url)  # TODO: Inconsistent output? Investigate.
    url_md5 = md5(str(url).encode('utf-8')).hexdigest()
    header_cache_filename = d + '/' + url_md5 + '.headers'  # TODO: Refractor path management
    with open(header_cache_filename, 'w') as header_cache_file:
        json.dump(url_header, header_cache_file)
