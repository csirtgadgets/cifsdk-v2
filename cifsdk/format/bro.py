
from cifsdk.format.plugin import Plugin
import re
from cifsdk.constants import PYVERSION

from pprint import pprint
otype = {
    'ipv4': 'ADDR',
    'url': 'URL',
    'fqdn': 'DOMAIN',
    'email': 'EMAIL',
    'md5': 'FILE_HASH',
    'sha1': 'FILE_HASH',
    'sha256': 'FILE_HASH',
}

HEADER = '#' + '\t'.join(['fields', 'indicator', 'indicator_type', 'meta.desc', 'meta.cif_confidence', 'meta.source'])
SEP = '|'


class Bro(Plugin):
    __name__ = 'bro'

    def __init__(self, *args, **kwargs):
        super(Bro, self).__init__(*args, **kwargs)

        self.cols = ['observable', 'otype', 'tags', 'confidence', 'provider']

    def __repr__(self):
        text = []
        for d in self.data:
            r = []
            if d['otype'] is 'url':
                d['observable'] = re.sub(r'(https?\:\/\/)', '', d['observable'])

            for c in self.cols:
                y = d.get(c, '-')
                if type(y) is list:
                    y = SEP.join(y)

                if isinstance(y, int):
                    y = str(y)

                if PYVERSION == 2:
                    if isinstance(y, unicode):
                        y = y.encode('utf-8')
                else:
                    if isinstance(y, bytes):
                        y = y.encode('utf-8')

                if c is 'otype':
                    y = 'Intel::{0}'.format(otype[d[c]])
                r.append(y)
            text.append("\t".join(r))

        text = "\n".join(text)
        
        text = "{0}\n{1}".format(HEADER, text)
        return text
