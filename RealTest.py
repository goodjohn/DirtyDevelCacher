#!/usr/bin/python3.4

from GetAndSave import fetch

test_urls = [
    'http://books.to_scrape.com',
    'http://books.toscrape.com/catalogue/',
    'http://books.toscrape.com/catalogue/algorithms-to-live-by-the-computer-science-of-human-decisions_880/',
    'http://books.toscrape.com/catalogue/category/books/travel_2/index.html',
    'http://books.toscrape.com/media/',
    'http://books.toscrape.com/media/cache/28/ea/28ea530a8b7955e422df64beaed7871a.jpg',
    'http://books.toscrape.com/media/cache/da/a0/daa08c54a927c27494ea5bb90af79c60.jpg',
    'http://books.toscrape.com/this-url-doesnt-exist',
    'http://quotes.toscrape.com/',
    'http://quotes.toscrape.com/tag/inspirational/',
    'http://quotes.toscrape.com/tag/deep-thoughts/',
    'http://quotes.toscrape.com/author/Albert-Einstein',
    'http://stuff.toscrape.com',
    'http://things.toscrape.com'
]

print(fetch(test_urls[10]).decode())
