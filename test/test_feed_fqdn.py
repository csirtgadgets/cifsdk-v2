import pytest


from cifsdk.feed.fqdn import Fqdn
from pprint import pprint

data = [
    'example.com',
    'test.example.com',
    'test.test.com',
    'csirtgadgets.org',
    'amazon.com',
    'test.amazon.com'
]

whitelist = [
    'example.com'
]


def test_feed_fqdn_whitelist():
    x = Fqdn()

    y = x.process(data, whitelist)

    assert 'example.com' not in y
    assert 'csirtgadgets.org' in y
    assert 'amazon.com' not in y

    # need to create the trie mod
    assert 'test.example.com' not in y
    assert 'test.amazon.com' not in y