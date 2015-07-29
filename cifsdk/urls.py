# -*- coding: utf-8 -*-

import re
# based on some of the work by https://github.com/giovino

# http://stackoverflow.com/questions/499345/regular-expression-to-extract-url-from-an-html-link
# RE for URL extraction:
# http://daringfireball.net/2010/07/improved_regex_for_matching_urls
# http://daringfireball.net/misc/2010/07/url-matching-regex-test-data.text
# https://gist.github.com/uogbuji/705383
# http://stackoverflow.com/questions/9760588/how-do-you-extract-a-url-from-a-string-using-python

RE_URL_PLAIN = r'(https?://[^\s>]+)'

from pprint import pprint


def _extract_urls_text(body):
    urls = set()
    found = re.findall(RE_URL_PLAIN, body)

    for u in found:
        urls.add(u)

    return urls


def _extract_urls_html(body):
    from bs4 import BeautifulSoup

    urls = set()
    soup = BeautifulSoup(body, "lxml")

    for link in soup.find_all('a'):
        if link.get('href'):
            urls.add(str(link.get('href')))

    return urls


def extract_urls(body, html=False):
    urls = set()

    if html:
        urls = _extract_urls_html(body)
    else:
        urls = _extract_urls_text(body)

    return urls
