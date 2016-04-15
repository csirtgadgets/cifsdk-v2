from cifsdk.format.plugin import Plugin
import csv

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class Csv(Plugin):

    def __init__(self, *args, **kwargs):
        super(Csv, self).__init__(*args, **kwargs)

    def __repr__(self):
        si = StringIO()
        cw = csv.writer(si, quoting=csv.QUOTE_ALL)
        cw.writerow(self.cols)
        for obs in self.data:
            r = []
            for c in self.cols:
                y = obs.get(c) or ''
                if type(y) is list:
                    y = ','.join(y)
                if type(y) == int:
                    y = str(y)
                if type(y) == float:
                    y = str(y)

                r.append(y.encode('utf-8'))
            cw.writerow(r)
        return si.getvalue().strip('\r\n')