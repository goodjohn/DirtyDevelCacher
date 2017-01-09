#!/usr/bin/python3.4

import GetAndSave

test_urls = [
    'http://books.toscrape.com/media/cache/28/ea/28ea530a8b7955e422df64beaed7871a.jpg',
    'http://books.toscrape.com/catalogue/algorithms-to-live-by-the-computer-science-of-human-decisions_880/',
    'http://books.toscrape.com/catalogue/',
    'http://things.toscrape.com'
]

for url in test_urls:
    GetAndSave.get_cache_path('cache_files_importer')
    GetAndSave.fetch(url)
    print()
