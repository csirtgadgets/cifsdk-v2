import pytest


from cifsdk.feed.ipv4 import Ipv4
from cifsdk.client import Client
from datetime import datetime
from pprint import pprint

data = [
    {
        'observable': '192.168.1.1',
        'tags': 'botnet',
        'reporttime': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'confidence': 85
    },
    {
        'observable': '192.168.2.1',
        'tags': 'malware',
        'reporttime': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'confidence': 85
    },
    {
        'observable': '128.205.1.1',
        'tags': 'scanner',
        'reporttime': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'confidence': 85
    },
    {
        'observable': '128.205.1.1',
        'tags': 'scanner',
        'reporttime': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'confidence': 75
    },
    {
        'observable': '128.205.2.0/24',
        'tags': 'scanner',
        'reporttime': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'confidence': 85
    },
    {
        'observable': '184.168.047.225/32',
        'tags': 'scanner',
        'reporttime': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'confidence': 85
    },
    {
        'observable': '1.0.0.0/1',
        'tags': 'hijacked',
        'reporttime': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'confidence': 85
    },
    {
        'observable': '1.0.0.0/8',
        'tags': 'hijacked',
        'reporttime': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'confidence': 85
    }
]

whitelist = [
    {
        'observable': '192.168.1.0/24',
        'tags': 'whitelist',
        'reporttime': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'confidence': 85
    },
    {
        'observable': '184.168.047.225/32',
        'tags': 'whitelist',
        'reporttime': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'confidence': 85
    },
]


def test_feed_ipv4_whitelist():
    x = Ipv4()

    s = set()
    for xx in x.process(data, whitelist):
        s.add(xx['observable'])

    assert '192.168.1.1' not in s
    assert '192.168.1.1' not in s
    assert '128.205.1.1' in s

    assert '1.0.0.0/1' not in s

    assert '1.0.0.0/8' in s


def test_feed_ipv4_confidence():
    x = Ipv4()
    cli = Client('http://localhost:5000', 1234)

    r = cli.aggregate(data, field='observable')
    r = x.process(r, whitelist)

    s = set()
    for rr in r:
        if rr['observable'] not in s:
            s.add(rr['confidence'])

    assert 75 not in s
