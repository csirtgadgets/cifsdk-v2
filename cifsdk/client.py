import ujson as json
import requests
import time
import logging

import sys
import os
import os.path
import yaml
import logging
import traceback
import select
from pprint import pprint
from cifsdk.format import factory

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import textwrap

from cifsdk import VERSION, API_VERSION

REMOTE ='https://localhost'
LIMIT = 5000


class Client(object):

    def __init__(self, token, remote=REMOTE, proxy=None, timeout=300, no_verify_ssl=False, nowait=False):
        
        self.logger = logging.getLogger(__name__)
        self.remote = remote
        self.token = str(token)
        self.proxy = proxy
        self.timeout = timeout
        
        if no_verify_ssl:
            self.verify_ssl = False
        else:
            self.verify_ssl = True

        self.session = requests.session()
        self.session.headers["Accept"] = "application/vnd.cif.v{0}+json".format(API_VERSION)
        self.session.headers['User-Agent'] = "py-cifsdk/{0}".format(VERSION)
        self.session.headers['Authorization'] = "Token token={0}".format(self.token)
        self.session.headers['Content-Type'] = 'application/json'

        self.nowait = nowait
    
    def search(self,decode=True, limit=LIMIT, nolog=None, filters={}, sort='lasttime'):
        filters['limit'] = limit
        filters['nolog'] = nolog
        
        uri = self.remote + '/observables'
            
        self.logger.debug('uri: %s' % uri)
        self.logger.debug('params: %s', json.dumps(filters))

        self.logger.info('searching...')

        try:
            body = self.session.get(uri, params=filters, verify=self.verify_ssl)
        except requests.exceptions.ConnectionError:
            self.logger.error('connection error')
            return None

        self.logger.debug('status code: ' + str(body.status_code))

        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            return 'request failed: %s' % str(body.status_code)

        ret = body.content
        if decode:
            self.logger.info('decoding...')
            ret = json.loads(ret)

            self.logger.info('sorting...')
            ret = sorted(ret, key=lambda o: o[sort])

        self.logger.debug('returning..')
        return ret

    def submit(self, data):
        """
        '{"observable":"example.com","confidence":"50",":tlp":"amber",
        "provider":"me.com","tags":["zeus","botnet"]}'
        """
        if not data:
            raise RuntimeError

        if not isinstance(data, basestring):
            if type(data) != list:
                data = [data]
            data = json.dumps(data)

        ##TODO - http://docs.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests
        uri = self.remote + '/observables'

        if self.nowait:
            uri = "{0}?nowait=1".format(uri)
        
        self.logger.debug('uri: %s' % uri)

        body = self.session.post(uri, data=data, verify=self.verify_ssl)
        self.logger.debug('status code: ' + str(body.status_code))
        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            self.logger.error(json.loads(body.text).get('message'))
            return None
        
        body = json.loads(body.text)
        return body
    
    def ping(self):
        t0 = time.time()
        uri = str(self.remote) + '/ping'
        body = self.session.get(uri, params={}, verify=self.verify_ssl)
        
        self.logger.debug('status code: ' + str(body.status_code))
        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            return 'request failed: %s' % str(body.status_code)
        
        t1 = (time.time() - t0)
        self.logger.debug('return time: %.15f' % t1)
        return t1


def main():

    p = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ cif --search example.com
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='cif'
    )

    # options
    p.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
    p.add_argument('-d', '--debug', dest='debug', action="store_true")
    p.add_argument('-V', '--version', action='version', version=VERSION)
    p.add_argument('--no-verify-ssl', action="store_true", default=False)
    p.add_argument('--remote',  help="remote api location (eg: https://example.com)")
    p.add_argument('--timeout',  help='connection timeout [default: %(default)s]', default="300")
    p.add_argument('-C', '--config',  help="configuration file [default: %(default)s]",
                   default=os.path.expanduser("~/.cif.yml"))

    p.add_argument('--sort', help='sort output ASC by key', default='reporttime')
    p.add_argument('--format', help="specify output format [default: %(default)s]", default="table")

    # actions
    p.add_argument('-p', '--ping', action="store_true", help="ping")
    p.add_argument('--submit', help="submit json string")

    # flags
    p.add_argument('--limit', help="result limit", default=500)
    p.add_argument('-n', '--nolog', help='do not log the search', default=None, action="store_true")

    # filters
    p.add_argument('-q', "--search", help="search for observable")
    p.add_argument('--firsttime', help='firsttime or later')
    p.add_argument('--lasttime', help='lasttime or earlier')
    p.add_argument('--reporttime', help='TODO')
    p.add_argument('--reporttimeend', help='TODO')
    p.add_argument("--tags", help="filter for tags")
    p.add_argument('--otype', help='filter by otype')
    p.add_argument("--cc", help="filter for countrycode")
    p.add_argument('--token', help="specify token")
    p.add_argument('--confidence', help="specify confidence")
    p.add_argument('--rdata', help='filter by rdata')
    p.add_argument('--provider', help='filter by provider')
    p.add_argument('--asn', help='filter by asn')

    # Process arguments
    args = p.parse_args()

    # setup the initial console logging
    fmt = '%(asctime)s - %(levelname)s - %(name)s::%(threadName)s - %(message)s'
    loglevel = logging.WARNING
    if args.verbose:
        loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(fmt))
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
    else:
        logger.info("{} config does not exist".format(args.config))

    if not options.get("remote"):
        logger.critical("missing --remote")
        raise SystemExit

    cli = Client(options['token'], remote=options['remote'], proxy=options.get('proxy'), no_verify_ssl=options[
        'no_verify_ssl'])

    try:
        if(options.get('search') or options.get('tags') or options.get('cc') or options.get('rdata') or options.get(
                'otype') or options.get('provider') or options.get('asn')):
            filters = {}
            if options.get('search'):
                filters['observable'] = options['search']
            if options.get('cc'):
                filters['cc'] = options['cc']

            if options.get('tags'):
                filters['tags'] = options['tags']

            if options.get('confidence'):
                filters['confidence'] = options['confidence']

            if options.get('firsttime'):
                filters['firsttime'] = options['firsttime']

            if options.get('lasttime'):
                filters['lasttime'] = options['lasttime']

            if options.get('reporttime'):
                filters['reporttime'] = options['reporttime']

            if options.get('reporttimeend'):
                filters['reporttimeend'] = options['reporttimeend']

            if options.get('otype'):
                filters['otype'] = options['otype']

            if options.get('rdata'):
                filters['rdata'] = options['rdata']

            if options.get('nolog'):
                options['nolog'] = 1

            if options.get('provider'):
                filters['provider'] = options['provider']

            if options.get('asn'):
                filters['asn'] = options['asn']

            ret = cli.search(limit=options['limit'], nolog=options['nolog'], filters=filters, sort=options.get('sort'))

            f = factory(options['format'])

            try:
                print(f(ret))
            except AttributeError as e:
                logger.exception(e)

        elif options.get('ping'):
            for num in range(0,4):
                ret = cli.ping()
                print "roundtrip: %s ms" % ret
                select.select([], [], [], 1)
        elif options.get('submit'):
            ret = cli.submit(options["submit"])
            f = factory(options['format'])

            try:
                print(f(ret))
            except AttributeError as e:
                logger.exception(e)
        else:
            logger.warning('operation not supported')
            sys.exit()

    except KeyboardInterrupt:
        raise SystemExit
    except Exception, e:
        logger.exception(e)
        raise SystemExit

if __name__ == "__main__":
    sys.exit(main())