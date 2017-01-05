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
elif not os.path.isdir(d):
    raise FileExistsError('Trouble creating cache directory.')

for url in urls.values():
    url_header = {}
    url_md5 = md5(str(url).encode('utf-8')).hexdigest()
    header_cache_filename = d + '/' + url_md5 + '.header'  # TODO: Refractor path management
    content_cache_filename = d + '/' + url_md5 + '.content'
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
    else:
        url_header['url'] = response.geturl()  # In case of redirects
        content = response.read()
        if os.path.isfile(content_cache_filename):
            with open(content_cache_filename, 'rb') as content_cache_file:
                print(content_cache_file.read())
        else:
            with open(content_cache_filename, 'wb') as content_cache_file:
                content_cache_file.write(content)
            print('Saved to cache.')
    with open(header_cache_filename, 'w') as header_cache_file:
        json.dump(url_header, header_cache_file)
