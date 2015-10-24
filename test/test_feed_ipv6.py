import pytest


from cifsdk.feed.ipv6 import Ipv6
from pprint import pprint
import logging

data = [
    '2001:4860:4860::8888'
]

whitelist = [
    '2001:4860:4860::8888',
]


def test_feed_ipv6_whitelist():
    pass # https://github.com/jsommers/pytricia/issues/6
    #x = Ipv6()
    #y = x.process(data, whitelist)
    #assert '2001:4860:4860::8888' not in y