#!/usr/bin/env python

try:
    import re2 as re
except ImportError:
    import re

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import email
import logging
import os.path
import textwrap
import sys
from cifsdk.client import Client
from cifsdk.observable import Observable

from pprint import pprint
import yaml


# http://stackoverflow.com/questions/499345/regular-expression-to-extract-url-from-an-html-link
# http://blog.magiksys.net/parsing-email-using-python-content
# https://github.com/mailgun/flanker
# https://pregmatch.org/read/python-procmail
# http://stackoverflow.com/questions/557906/want-procmail-to-run-a-custom-python-script-everytime-a-new-mail-shows-up
# http://stackoverflow.com/questions/14676375/pipe-email-from-procmail-to-python-script-that-parses-body-and-saves-as-text-fil

# read
# http://blog.magiksys.net/parsing-email-using-python-content
# https://github.com/andris9/mailparser

# RE for URL extraction:
# http://daringfireball.net/2010/07/improved_regex_for_matching_urls
# http://daringfireball.net/misc/2010/07/url-matching-regex-test-data.text
# https://gist.github.com/uogbuji/705383
# GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([
# ^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'

# re.compile(r'http.?://[a-z,/,\.,\d,\?,=,\-,\+,#,_,&,;,\,,:,@,%,]*', re.IGNORECASE).findall(xxx)
RE_URL = r'href=[\'"]?([^\'" >]+)'
REPLACE = ['=\n', "\t", "\r", '\\n']
REMOTE_DEFAULT = "http://localhost:5000"


def extract_urls(msg):
    msg = msg.replace("=3D", '=')
    for x in REPLACE:
        msg = msg.replace(x, '')

    urls = re.findall(RE_URL, msg)

    links = {u.lower() for u in urls}
    return links


def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ cat test.eml | cif-procmail -v
            $ cif-procmail --file test.eml
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='cif-procmail'
    )

    p.add_argument("-v", "--verbose", dest="verbose", action="count",
                   help="set verbosity level [default: %(default)s]")
    p.add_argument('-d', '--debug', dest='debug', action="store_true")

    p.add_argument("-f", "--file", dest="file", help="specify email file")

    # cif arguments
    p.add_argument("--confidence", help="specify confidence for submitting to CIF", default="65")
    p.add_argument("--remote", help="specify CIF remote [default: %(default)s",
                   default=REMOTE_DEFAULT)
    p.add_argument("--token", help="specify CIF token")
    p.add_argument("--config", help="specify CIF config [default: %(default)s",
                   default=os.path.expanduser("~/.cif.yml"))
    p.add_argument("--tags", help="specify CIF tags [default: %(default)s", default=["phishing"])
    p.add_argument("--group", help="specify CIF group [default: %(default)s", default="everyone")
    p.add_argument("--tlp", help="specify CIF TLP [default: %(default)s", default="amber")
    p.add_argument("--no-verify-ssl", action="store_true", default=False)
    p.add_argument("--raw", help="include raw message data")
    p.add_argument("--raw-headers", help="include raw header data", action="store_true")
    p.add_argument("--provider", help="specify feed provider [default: %(default)s", default="localhost")


    args = p.parse_args()

    loglevel = logging.WARNING
    if args.verbose:
        loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)

    options = vars(args)

    if os.path.isfile(args.config):
        f = file(args.config)
        config = yaml.load(f)
        f.close()
        if not config['client']:
            raise Exception("Unable to read " + args.config + " config file")
        config = config['client']
        for k in config:
            if not options.get(k):
                options[k] = config[k]

        if config.get("remote") and options["remote"] == REMOTE_DEFAULT:
            options["remote"] = config["remote"]

    else:
        logger.info("{} config does not exist".format(args.config))

    if not options.get("remote"):
        logger.critical("missing --remote")
        raise SystemExit

    if options.get("file"):
        with open(options["file"]) as f:
            msg = email.message_from_file(f)
    else:
        msg = sys.stdin.read()
        msg = email.message_from_string(msg)

    html = msg.get_payload()
    urls = extract_urls(html)

    logger.debug(pprint(urls))
    cli = Client(remote=options["remote"], token=options["token"], no_verify_ssl=options["no_verify_ssl"])

    for u in urls:
        logger.info("submitting: {}".format(u))
        raw = html
        if options.get("raw_headers"):
            raw = msg.as_string()
        o = Observable(
            observable=u,
            confidence=options["confidence"],
            tlp=options["tlp"],
            group=options["group"],
            tags=options["tags"],
            raw=raw,
            provider=options["provider"]
        )
        r = cli.submit(submit=str(o))
        print r


if __name__ == "__main__":
    main()