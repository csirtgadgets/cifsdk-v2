from cifsdk.format.plugin import Plugin
import re
import os
from pprint import pprint

SID = os.environ.get('CIF_SNORT_SID', 5000000000)
THRESHOLD = os.environ.get('CIF_SNORT_THRESHOLD', 'type limit,track by_src,count 1,seconds 3600')
SRC = os.environ.get('CIF_SNORT_SRC', 'any')
DEST = os.environ.get('CIF_SNORT_DST', 'any')
MSG_PREFIX = os.environ.get('CIF_SNORT_MSG_PREFIX', 'CIF')
TLP_DEFAULT = os.environ.get('CIF_SNORT_TLP', 'GREEN')
PRIORITY = os.environ.get('CIF_SNORT_PRIOIRTY', 1)
CLASSTYPE = os.environ.get('CIF_SNORT_CLASSTYPE', False)
TAG = os.environ.get('CIF_SNORT_TAG', False)

# https://github.com/csirtgadgets/p5-cif-sdk/blob/master/lib/CIF/SDK/Format/Snort.pm
# https://github.com/csirtgadgets/p5-snort-rule/blob/master/lib/Snort/Rule.pm
class Snort(Plugin):
    __name__ = 'cifsnort'

    def __init__(self, *args, **kwargs):
        super(Snort, self).__init__(*args, **kwargs)

        self.cols = ['observable', 'otype', 'tags', 'confidence', 'provider']

    def _dict_to_rule(self, rule, opts=False):
        r = ' '.join([
            rule['action'],
            rule['proto'],
            rule['src'],
            rule['sport'],
            rule['dir'],
            rule['dst'],
            rule['dport'],
        ])

        if opts:
            opstring = '; '.join('{}: {}'.format(v, opts[v]) for v in opts if opts[v])
            r = '{} ({};)'.format(r, opstring)

        return r

    def __repr__(self):
        text = []
        sid = SID
        for d in self.data:
            r = {
                'action': 'alert',
                'proto': d.get('protocol', 'IP'),
                'src': SRC,
                'sport': 'any',
                'dir': '->',
                'dst': d['observable'],
                'dport': d.get('portlist', 'any'),
            }

            opts = {
                'msg': '{} - {} - {}'.format(MSG_PREFIX, TLP_DEFAULT, ','.join(d['tags'])),
                'sid': sid,
                'threshold': THRESHOLD,
                'classtype': CLASSTYPE,
                'reference': d.get('altid', ''),
                'priority': PRIORITY,
                'tag': TAG,

            }

            if d['otype'] == 'ipv4':
                pass

            if d['otype'] == 'ipv4':
                pass

            if d['otype'] == 'fqdn':
                pass

            if d['otype'] == 'url':
                pass

            text.append(self._dict_to_rule(r, opts))
            sid += 1

        return "\n".join(text)
