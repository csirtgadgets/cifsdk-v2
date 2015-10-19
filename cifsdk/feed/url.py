#from cifsdk.feed import tag_contains_whitelist


class Url(object):

    def __init__(self):
        pass

    def process(self, data, whitelist):

        wl = set()
        for x in whitelist:
            wl.add(x)

        rv = set()
        for x in data:
            if tag_contains_whitelist(x['tags']):
                continue

            if x not in wl:
                rv.add(x)

        return rv



