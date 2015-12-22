COLUMNS = ['tlp', 'reporttime', 'observable', 'otype', 'cc', 'asn', 'asn_desc', 'confidence', 'description', 'tags',
           'rdata', 'provider']
MAX_FIELD_SIZE = 30


class Plugin(object):

    def __init__(self, data=[], cols=COLUMNS, max_field_size=MAX_FIELD_SIZE):
        from pprint import pprint

        self.cols = cols
        self.max_field_size = max_field_size
        self.data = data
        if self.data:
            if type(self.data) is not list:
                self.data = [self.data]
        else:
            self.data = []

    def __repr__(self):
        raise NotImplementedError