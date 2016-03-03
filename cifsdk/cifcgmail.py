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

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'
CONFIDENCE = 50
TLP = 'green'
PROVIDER = 'localhost'


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

    p.add_argument('--url-ignore', help='url patterns to ignore')

     # Process arguments
    args = p.parse_args()
    setup_logging(args)
    logger = logging.getLogger(__name__)

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

    for u in urls:
        u = u.rstrip('\/')
        logger.info("submitting: {0}".format(u))

        o = Observable(
            observable=u,
            confidence=options["confidence"],
            tlp=options["tlp"],
            group=options["group"],
            tags=options["tags"],
            provider=options.get('provider')
        )

        o = o.__dict__
        del o['logger']

        if options.get('raw'):
            o.raw = email

        r = cli.submit(o)
        logger.info("submitted: {0}".format(r))


if __name__ == "__main__":
    main()
