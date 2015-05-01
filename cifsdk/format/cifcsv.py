from cifsdk.format import Plugin
import csv
import StringIO


class Csv(Plugin):

    def __init__(self, *args, **kwargs):
        super(Csv, self).__init__(*args, **kwargs)

    def __repr__(self):
        si = StringIO.StringIO()
        cw = csv.writer(si)
        for obs in self.data:
            r = []
            for c in self.cols:
                y = obs.get(c) or ''
                if type(y) is list:
                    y = ','.join(y)
                y = str(y)
                y = (y[:self.max_field_size] + '..') if len(y) > self.max_field_size else y
                r.append(y)
            cw.writerow(r)
        return si.getvalue().strip('\r\n')