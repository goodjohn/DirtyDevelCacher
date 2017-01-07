#!/usr/bin/python3.4

import urllib
from urllib.request import urlopen
from pprint import pprint
import json
import os
from hashlib import md5
import time

# TODO: !!! Definitely needs a refactor now.

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

for desc, url in urls.items():
    print('{:<12} : '.format(desc), end='')
    content = ''
    url_header = {}
    url_md5 = md5(str(url).encode('utf-8')).hexdigest()
    header_cache_filename = os.path.join(d, url_md5+'.header')
    content_cache_filename = os.path.join(d, url_md5+'.content')
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
    with open(header_cache_filename, 'w') as header_cache_file:
        json.dump(url_header, header_cache_file)
    if os.path.isfile(header_cache_filename) and time.time() - os.path.getmtime(header_cache_filename) < 180:
        decode = False
        with open(header_cache_filename, 'r') as header_file:
            header_info = json.load(header_file)
        if 'Content-Type' in header_info and header_info['Content-Type'] == 'text/html':
            decode = True
        if not header_info['net_conn']:
            print('Bad network connection; resource not in cache')
        elif header_info['status'] == 404 or header_info['status'] == 403:
            print('HTTP Status {}; resource not in cache.'.format(header_info['status']))
        elif os.path.isfile(content_cache_filename):
            with open(content_cache_filename, 'rb') as content_cache_file:
                if decode:
                    # print(content_cache_file.read().decode())
                    print('Content available for decoding.')
                else:
                    # print(content_cache_file.read())
                    print('Content available.')
    elif content:
        with open(content_cache_filename, 'wb') as content_cache_file:
            content_cache_file.write(content)
        print('Saved to cache: ', content_cache_filename)
