#!/usr/bin/python3.4

import json
import os
import time
import urllib
from hashlib import md5
from urllib.request import urlopen

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


def get_filename(path, name, ext):
    name_ = md5(str(name).encode('utf-8')).hexdigest()
    full = os.path.join(path, name_+ext)
    return full


def fetch_from_web(url):
    print('[Web]   ', end='')
    content_cache_filename = get_filename(d, url, '.content')
    header_cache_filename = get_filename(d, url, '.header')
    url_header = {}
    try:
        response = urlopen(url)
        url_header = dict(response.info())
        url_header['net_conn'] = True
        url_header['status'] = response.status
    except urllib.error.HTTPError as e:
        url_header['net_conn'] = True
        url_header['status'] = e.status
        print('Failed: Bad HTTP status {}.'.format(e.status))
    except urllib.error.URLError as e:
        url_header['net_conn'] = False
        url_header['reason'] = '{}'.format(e.reason)
        print('Failed: Bad network connection; {}.'.format(e.reason))
    else:
        url_header['url'] = response.geturl()  # In case of redirects
        with open(content_cache_filename, 'wb') as content_cache_file:
            content_cache_file.write(response.read())
        print('Success: saved to cache:', content_cache_filename)
    with open(header_cache_filename, 'w') as header_cache_file:
        json.dump(url_header, header_cache_file)


def fetch_from_cache(url, max_age=180):
    print('[Cache] ', end='')
    content_cache_filename = get_filename(d, url, '.content')
    header_cache_filename = get_filename(d, url, '.header')
    if os.path.isfile(header_cache_filename) and time.time() - os.path.getmtime(header_cache_filename) < max_age:
        with open(header_cache_filename, 'r') as header_file:
            header_info = json.load(header_file)
        if not header_info['net_conn']:
            print('Failed: Bad network connection; resource not in cache')
        elif header_info['status'] == 404 or header_info['status'] == 403:
            print('Failed: HTTP Status {}; resource not in cache.'.format(header_info['status']))
        elif os.path.isfile(content_cache_filename):
            with open(content_cache_filename, 'rb') as content_cache_file:
                # print(content_cache_file.read())
                print('Success: Content available.')
            return True
    else:
        if not os.path.isfile(header_cache_filename):
            print('Failed: File not found.')
        elif time.time() - os.path.getmtime(header_cache_filename) < max_age:
            print('Failed: Resource exceeds maximum age.')
    return False


for desc, url in urls.items():
    print('_'*80)
    print(' ', desc)
    if not fetch_from_cache(url):
        fetch_from_web(url)
    print('\u203e'*80)
    print()



