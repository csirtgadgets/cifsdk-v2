import pytest


from cifsdk.feed.ipv6 import Ipv6
from pprint import pprint
import logging

data = [
    {
        'observable': '2001:4860:4860::8888',
        'tags': 'botnet',
    }
]

whitelist = [
    {
        'observable': '2001:4860:4860::8888',
        'tags': 'whitelist',
    }
]


def test_feed_ipv6_whitelist():
    #pass # https://github.com/jsommers/pytricia/issues/6
    x = Ipv6()
    s = set()
    for xx in x.process(data, whitelist):
        s.add(xx['observable'])

    assert '2001:4860:4860::8888' not in s