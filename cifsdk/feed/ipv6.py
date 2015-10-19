#from cifsdk.feed import tag_contains_whitelist
import pytricia
import logging
from pprint import pprint

PERM_WHITELIST = [
    ## TODO -- more
    # http://www.iana.org/assignments/ipv6-multicast-addresses/ipv6-multicast-addresses.xhtml
    # v6
    'FF01:0:0:0:0:0:0:1',
    'FF01:0:0:0:0:0:0:2',
]


class Ipv6(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        pass

    # https://github.com/jsommers/pytricia
    # https://github.com/fnl/patricia-trie/blob/master/patricia.py
    def process(self, data, whitelist):
        raise RuntimeError('https://github.com/jsommers/pytricia/issues/6')
        print('setting up trie')
        wl = pytricia.PyTricia()

        print('adding perm whitelist')
        [wl.insert(x, True) for x in PERM_WHITELIST]

        print('adding submitted whitelist')
        [wl.insert(y, True) for y in whitelist]

        return (y for y in data if y not in wl)




