import pytest


from cifsdk.feed.ipv4 import Ipv4
from pprint import pprint

data = [
    '192.168.1.1',
    '192.168.2.1',
    '128.205.1.1',
]

whitelist = [
    '192.168.1.0/24'
]


def test_feed_ipv4_whitelist():
    x = Ipv4()

    y = x.process(data, whitelist)

    assert '128.205.1.1' in y
    assert '192.168.1.1' not in y