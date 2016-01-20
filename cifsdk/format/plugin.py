from cifsdk.constants import FIELDS
MAX_FIELD_SIZE = 30


class Plugin(object):

    def __init__(self, data=[], cols=FIELDS, max_field_size=MAX_FIELD_SIZE):
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