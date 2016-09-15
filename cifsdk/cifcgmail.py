#!/usr/bin/env python

try:
    import cgmail
except ImportError:
    print('py-cgmail needs to be installed: https://github.com/csirtgadgets/py-cgmail')

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import logging
import os.path
import textwrap
import sys
from pprint import pprint

from cifsdk.utils import setup_logging, read_config
from cifsdk.client import Client
from cifsdk.observable import Observable
import re
import arrow
from cgmail.urls import url_to_fqdn

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'
CONFIDENCE = 50
TLP = 'green'
PROVIDER = 'localhost'

EXCLUDE = os.environ.get('CGMAIL_EXCLUDE', None)
CONFIDENCE_LOWER = os.environ.get('CGMAIL_CONFIDENCE_LOWER', None)
WHITELIST_CACHE = os.environ.get('CGMAIL_WHITELIST_CACHE', '/tmp/cgmail_whitelist.txt')
BLACKLIST_CACHE = os.environ.get('CGMAIL_BLACKLIST_CACHE', '/tmp/cgmail_blacklist.txt')

URL_SHORTNERS = (
    'tinyurl.com',
    'goo.gl',
)

HOSTING_PROVIDERS = (
    'esy.es'
)


def match_whitelist(wl, d):
    bits = d.split('.')
    bits2 = list(bits)

    for i, b in enumerate(bits2):
        if '.'.join(bits) in wl:
            return True
        bits.pop(0)


def main():

    #
    # initialize module
    #

    p = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ cat test.eml | cgmail
            $ cgmail --file test.eml
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='cgmail'
    )

    p.add_argument("-v", "--verbose", dest="verbose", action="count",
                   help="set verbosity level [default: %(default)s]")
    p.add_argument('-d', '--debug', dest='debug', action="store_true")

    p.add_argument("-f", "--file", dest="file", help="specify email file")

    # cif arguments
    p.add_argument("--confidence", help="specify confidence for submitting to CIF", default=CONFIDENCE)
    p.add_argument("--remote", help="specify CIF remote")
    p.add_argument("--token", help="specify CIF token")
    p.add_argument("--config", help="specify CIF config [default: %(default)s",
                   default=os.path.expanduser("~/.cif.yml"))
    p.add_argument("--tags", help="specify CIF tags [default: %(default)s", default=["phishing"])
    p.add_argument("--group", help="specify CIF group [default: %(default)s", default="everyone")
    p.add_argument("--tlp", help="specify CIF TLP [default: %(default)s", default=TLP)
    p.add_argument("--no-verify-ssl", action="store_true", default=False)
    p.add_argument("--raw", action="store_true", help="include raw message data")
    p.add_argument("--provider", help="specify feed provider [default: %(default)s]", default=PROVIDER)

    p.add_argument('--exclude', help='url patterns to exclude [default: %(default)s', default=EXCLUDE)
    p.add_argument('--confidence-lower', help='patterns to automatically lower confidence', default=CONFIDENCE_LOWER)
    p.add_argument('-n', '--not-really', help='do not submit', action='store_true')
    p.add_argument('--cache', help='location to cache whitelist [default: %(default)s', default=WHITELIST_CACHE)
    p.add_argument('--blacklist-cache', default=BLACKLIST_CACHE)

     # Process arguments
    args = p.parse_args()
    setup_logging(args)
    logger = logging.getLogger(__name__)

    exclude = None
    if args.exclude:
        exclude = re.compile(args.exclude)

    confidence_lower = None
    if args.confidence_lower:
        confidence_lower = re.compile(args.confidence_lower)

    o = read_config(args)
    options = vars(args)
    for v in options:
        if options[v] is None:
            options[v] = o.get(v)

    if not options.get('token'):
        raise RuntimeError('missing --token')

    if options.get("file"):
        with open(options["file"]) as f:
            email = f.read()
    else:
        email = sys.stdin.read()

    # extract urls from message body and mail parts
    bits = cgmail.parse_email_from_string(email)
    urls = set()

    for n in bits:
        if n.get('urls'):
            for u in n['urls']:
                urls.add(u)

    verify_ssl = True
    if options.get('no_verify_ssl'):
        verify_ssl = False

    # initialize cif client
    cli = Client(remote=options["remote"], token=options["token"], verify_ssl=verify_ssl)

    update_cache = True
    if os.path.isfile(args.cache):
        modified = os.path.getmtime(args.cache)
        if arrow.utcnow() < arrow.get(modified + 84600):
            update_cache = False

    if update_cache:
        # pull FQDN whitelist

        filters = {
            'tags': 'whitelist',
            'otype': 'fqdn',
            'confidence': 25,
        }
        now = arrow.utcnow()
        filters['reporttimeend'] = '{0}Z'.format(now.format('YYYY-MM-DDTHH:mm:ss'))
        now = now.replace(days=-7)
        filters['reporttime'] = '{0}Z'.format(now.format('YYYY-MM-DDTHH:mm:ss'))

        ret = cli.search(limit=50000, filters=filters, sort='reporttime', sort_direction='desc')
        with open(args.cache, 'w') as f:
            for r in ret:
                f.write("{0}\n".format(r['observable']))

    update_cache = True
    if os.path.isfile(args.blacklist_cache):
        modified = os.path.getmtime(args.blacklist_cache)
        if arrow.utcnow() < arrow.get(modified + 84600):
            update_cache = False

    if update_cache:
        filters = {
            'tags': 'phishing,suspicious,malware',
            'otype': 'fqdn',
            'confidence': 75,
        }
        now = arrow.utcnow()
        filters['reporttimeend'] = '{0}Z'.format(now.format('YYYY-MM-DDTHH:mm:ss'))
        now = now.replace(days=-7)
        filters['reporttime'] = '{0}Z'.format(now.format('YYYY-MM-DDTHH:mm:ss'))

        ret = cli.search(limit=50000, filters=filters, sort='reporttime', sort_direction='desc')
        with open(args.blacklist_cache, 'w') as f:
            for r in ret:
                f.write("{0}\n".format(r['observable']))

    fqdns = set()
    with open(args.cache) as f:
        for l in f:
            fqdns.add(l.rstrip("\n"))

    fqdns_blacklist = set()
    with open(args.blacklist_cache) as f:
        for l in f:
            fqdns_blacklist.add(l.rstrip("\n"))

    for u in urls:
        u = u.rstrip('\/')
        u = urlparse(u)

        fqdn = url_to_fqdn(u.geturl())
        if exclude and exclude.search(fqdn):
            continue

        confidence = options['confidence']

        if match_whitelist(fqdns, u.netloc):
            if (u.netloc not in URL_SHORTNERS) and (not match_whitelist(HOSTING_PROVIDERS, u.netloc)):
                confidence = options['confidence'] - 15
            else:
                confidence = options['confidence'] + 5
        elif match_whitelist(fqdns_blacklist, u.netloc):
            confidence = options['confidence'] + 10
        else:
            confidence = options['confidence'] + 5

        # else
        # raise confidence
        logger.info("submitting: {0}".format(u.geturl()))

        o = Observable(
            observable=u.geturl(),
            confidence=confidence,
            tlp=options["tlp"],
            group=options["group"],
            tags=options["tags"],
            provider=options.get('provider')
        )

        o = o.__dict__
        del o['logger']

        if options.get('raw'):
            o.raw = email

        if not args.not_really:
            r = cli.submit(o)
            logger.info("submitted: {0}".format(r))


if __name__ == "__main__":
    main()
