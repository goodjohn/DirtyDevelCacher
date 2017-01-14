#!/usr/bin/python3.4
import http
import inspect
import json
import os
import time
import urllib
from hashlib import md5
from urllib.request import urlopen


class GetAndSave:

    def __init__(self, url, cache_path='cache_files_default', max_age=180, verbose=True):
        self.url = url
        self.cache_path = cache_path
        self.content_file = url
        self.header_file = url
        self.max_age = max_age
        self.verbose_toggle = verbose

    @property
    def cache_path(self):
        return self.__cache_path

    @cache_path.setter
    def cache_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            raise FileExistsError('Trouble creating cache directory.')
        self.__cache_path = path

    @property
    def header_file(self):
        return self.__header_file

    @header_file.setter
    def header_file(self, url):
        hashed_name = md5(str(url).encode('utf-8')).hexdigest() + '.header'
        full = os.path.join(self.cache_path, hashed_name)
        self.__header_file = full

    @property
    def content_file(self):
        return self.__content_file

    @content_file.setter
    def content_file(self, url):
        hashed_name = md5(str(url).encode('utf-8')).hexdigest() + '.content'
        full = os.path.join(self.cache_path, hashed_name)
        self.__content_file = full

    def fetch_from_web(self):
        self.verbose('[Web]   ', end='')
        url_header = {}
        try:
            response = urlopen(self.url)
            url_header = dict(response.info())
            url_header['net_conn'] = True
            url_header['status'] = response.status
        except urllib.error.HTTPError as e:
            url_header['net_conn'] = True
            url_header['status'] = e.status
            self.verbose('Failed : Bad HTTP status {}.'.format(e.status))
        except urllib.error.URLError as e:
            url_header['net_conn'] = False
            url_header['reason'] = '{}'.format(e.reason)
            self.verbose('Failed : Bad network connection; {}.'.format(e.reason))
        except http.client.BadStatusLine as e:
            url_header['net_conn'] = False
            self.verbose('Failed : Unknown HTTP status code; URL is probably invalid. (http.client.BadStatusLine, {})'.format(e))
        else:
            url_header['url'] = response.geturl()  # In case of redirects
            with open(self.content_file, 'wb') as content_cache_file:
                content_cache_file.write(response.read())
            self.verbose('Success: saved to cache:', self.content_file)
        with open(self.header_file, 'w') as header_cache_file:
            json.dump(url_header, header_cache_file)
        return url_header['net_conn'] and url_header['status'] == 200

    def fetch_from_cache(self):
        self.verbose('[Cache] ', end='')
        age = time.time() - os.path.getmtime(self.header_file)
        if os.path.isfile(self.header_file) and age < self.max_age:
            with open(self.header_file, 'r') as header_file:
                header_info = json.load(header_file)
            if not header_info['net_conn']:
                self.verbose('Failed : Bad network connection; resource not in cache')
            elif header_info['status'] == 404 or header_info['status'] == 403:
                self.verbose('Failed : HTTP Status {}; resource not in cache.'.format(header_info['status']))
            elif os.path.isfile(self.content_file):
                with open(self.content_file, 'rb') as content_cache_file:
                    # self.verbose(content_cache_file.read())
                    size = os.path.getsize(self.content_file)
                    self.verbose('Success: Content available ({} KB).'.format(round(size / 1024)))
                return True
        else:
            if not os.path.isfile(self.header_file):
                self.verbose('Failed : File not found.')
            elif age >= self.max_age:
                self.verbose('Failed : Resource exceeds maximum age.')
            return None
        return False

    def fetch(self):
        c = self.fetch_from_cache()
        if c is None:
            c = self.fetch_from_web()
        elif c is False:
            self.verbose(' '*17 + 'Bad URL. Check and try again: {}'.format(self.url))
        return c

    def verbose(self, message, *args, **kwargs):
        if self.verbose_toggle:
            print(message, *args, **kwargs)


def debug_pprint(urls, max_age):
    print()
    print('>>', inspect.stack()[-1][1])
    if os.popen('which stty').read():
        rows, columns = os.popen('stty size', 'r').read().split()
        width = int(columns)
    else:
        width = 100  # Approximate minimum debug output length/width
    for url in urls:
        f = GetAndSave(url, max_age=max_age)
        print('_' * width)
        f.fetch()
        print('\u203e' * width)


if __name__ == '__main__':
    test_urls = [
        'http://books.toscrape.com/catalogue/category/books/travel_2/index.html',
        'http://books.toscrape.com/media/cache/da/a0/daa08c54a927c27494ea5bb90af79c60.jpg',
        'http://books.toscrape.com/this-url-doesnt-exist',
        'http://books.toscrape.com/media/',
        'http://books.to_scrape.com',
        'http://stuff.toscrape.com',
        'http://quotes.toscrape.com/',
        'http://quotes.toscrape.com/tag/inspirational/',
        'http://quotes.toscrape.com/author/Albert-Einstein'
    ]
    debug_pprint(test_urls, 30)
