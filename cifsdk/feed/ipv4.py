from cifsdk.feed import tag_contains_whitelist
import pytricia

from pprint import pprint

PERM_WHITELIST = [
    "0.0.0.0/8",
    "10.0.0.0/8",
    "127.0.0.0/8",
    "192.168.0.0/16",
    "169.254.0.0/16",
    "192.0.2.0/24",
    "224.0.0.0/4",
    "240.0.0.0/5",
    "248.0.0.0/5",
]


class Ipv4(object):

    def __init__(self):
        pass

    # https://github.com/jsommers/pytricia
    def process(self, data, whitelist):
        wl = pytricia.PyTricia()
        for x in PERM_WHITELIST:
            wl.insert(x, True)

        [wl.insert(y, True) for y in whitelist]

        return (y for y in data if y not in wl)




