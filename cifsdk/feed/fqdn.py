from cifsdk.feed import tag_contains_whitelist
import pytricia

from pprint import pprint

PERM_WHITELIST = [
    'google.com',
    'yahoo.com',
    'facebook.com',
    'youtube.com',
    'netflix.com',
    'baidu.com',
    'wikipedia.org',
    'twitter.com',
    'qq.com',
    'taobao.com',
    'amazon.com',
    'live.com',
    'bing.com',
    'wordpress.com',
    'msn.com',
]


def match(fqdn, data):
    if fqdn in data:
        return True


class Fqdn(object):

    def __init__(self):
        pass

    # https://github.com/jsommers/pytricia
    def process(self, data, whitelist):

        wl = set()
        for x in PERM_WHITELIST:
            wl.add(x)

        for x in whitelist:
            wl.add(x)

        rv = set()
        for x in data:
            if x not in wl:
                rv.add(x)

        pprint(rv)
        return rv



