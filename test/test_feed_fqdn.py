import pytest


from cifsdk.feed.fqdn import Fqdn
from pprint import pprint

data = [
    {
        'observable': 'example.com',
        'tags': 'botnet',
    },
    {
        'observable': 'test.example.com',
        'tags': 'malware',
    },
    {
        'observable': 'test.test.com',
        'tags': 'scanner'
    },
    {
        'observable': 'amazon.com',
        'tags': 'scanner'
    },
    {
        'observable': 'test.amazon.com',
        'tags': 'scanner'
    },
        {
        'observable': 'csirtgadgets.org',
        'tags': 'scanner'
    },
    {
        'observable': 'evil.org',
        'tags': 'scanner'
    },
    {
        'observable': 'gmail-smtp-in.l.google.com',
        'tags': 'malware'
    }
]

whitelist = [
    {
        'observable': 'example.com',
    },
    {
        'observable': 'google.com',
    }
]


def test_feed_fqdn_whitelist():
    x = Fqdn()

    y = x.process(data, whitelist)

    s = set()

    for xx in x.process(data, whitelist):
        s.add(xx['observable'])

    assert 'example.com' not in s
    assert 'csirtgadgets.org' in s
    assert 'amazon.com' not in s

    # need to create the trie mod
    assert 'test.example.com' not in s
    assert 'test.amazon.com' not in s
    assert 'amazon.com' not in s
    assert 'evil.org' in s

    assert 'gmail-smtp-in.l.google.com' not in s