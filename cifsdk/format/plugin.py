COLUMNS = ['reporttime', 'observable', 'cc', 'asn', 'asn_desc', 'confidence', 'tags', 'rdata', 'provider']
MAX_FIELD_SIZE = 30


class Plugin(object):

    def __init__(self, data=[], cols=COLUMNS, max_field_size=MAX_FIELD_SIZE):
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