import pytest


from cifsdk.feed.ipv4 import Ipv4
from pprint import pprint

data = [
    {
        'observable': '192.168.1.1',
        'tags': 'botnet',
    },
    {
        'observable': '192.168.2.1',
        'tags': 'malware',
    },
    {
        'observable': '128.205.1.1',
        'tags': 'scanner'
    },
    {
        'observable': '128.205.2.0/24',
        'tags': 'scanner'
    },
    {
        'observable': '184.168.047.225/32',
        'tags': 'scanner'
    },
]

whitelist = [
    {
        'observable': '192.168.1.0/24',
        'tags': 'whitelist'
    },
    {
        'observable': '184.168.047.225/32',
        'tags': 'whitelist'
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