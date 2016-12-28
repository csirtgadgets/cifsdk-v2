import ujson as json
import time
import sys
import os
import os.path
import yaml
import logging
import select
from cifsdk.format import factory as format_factory
from cifsdk.feed import factory as feed_factory
from cifsdk.format import plugins as FORMATS

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from signal import signal, SIGPIPE, SIG_DFL
import textwrap
import copy
import arrow
import zlib
import base64

from cifsdk import VERSION, API_VERSION
from cifsdk.constants import REMOTE_ADDR, REMOTE_ADDR_DEFAULT, LIMIT, FEED_CONFIDENCE, WHITELIST_LIMIT, PROXY, \
    FEED_LIMIT, TOKEN, FIELDS
from cifsdk.constants import PINGS, WHITELIST_CONFIDENCE
from cifsdk.utils import setup_logging, read_config
from time import sleep

# https://urllib3.readthedocs.org/en/latest/security.html#disabling-warnings
# http://stackoverflow.com/questions/14789631/hide-userwarning-from-urllib2
import requests
requests.packages.urllib3.disable_warnings()


RETRIES = os.environ.get('CIFSDK_RETRIES', 4)
RETRY_SLEEP = 5


class Client(object):

    def __init__(self, token, remote=REMOTE_ADDR, proxy=None, timeout=300, verify_ssl=True, nowait=False):
        """
        Initiates a client object

        :param token: <cif token> (ex: 6e10366ce0a25227aac810b4058c3712d30d3848f4d5d8f586658178a65c67df)
        :param remote: server location (ex: https://localhost)
        :param proxy: proxy server location
        :param timeout: seconds for client timeout (default: 300)
        :param no_verify_ssl: turn off TLS verification (default: False)
        :param nowait: batch submissions on the server, do not wait for returned submission id's. Best to
               to use this if submitting more than 100 records at a time. (default: False)
        :return: object
        """
        
        self.logger = logging.getLogger(__name__)
        self.remote = remote
        self.token = str(token)
        self.proxy = proxy
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        self.session = requests.session()
        self.session.headers["Accept"] = "application/vnd.cif.v{0}+json".format(API_VERSION)
        self.session.headers['User-Agent'] = "py-cifsdk/{0}".format(VERSION)
        self.session.headers['Authorization'] = "Token token={0}".format(self.token)
        self.session.headers['Content-Type'] = 'application/json'

        self.nowait = nowait
    
    def search(self, query=None, filters={}, limit=None, nolog=None, sort='lasttime', sort_direction='ASC', decode=True):
        """returns search result set based on either query or filters

        :param query: a single observable (ex: example.com, 192.168.1.1, ...)
        :param filters: filter results by various attributes: https://github.com/csirtgadgets/massive-octo-spice/wiki/API
        :param limit: limit return results
        :param nolog: do NOT log query
        :param sort: sort result set (default: 'lasttime')
        :param decode: decode the results from JSON (default: yes)
        :return: list of dicts (observables)
        """
        filters['limit'] = limit
        filters['nolog'] = nolog
        filters['gzip'] = 1

        if query:
            filters['observable'] = query

        if filters.get('observable'):
            filters['observable'] = filters['observable'].lower()
        
        uri = self.remote + '/observables'

        if filters.get('tags') and type(filters.get('tags')) is list:
            filters['tags'] = ','.join(filters['tags'])

        if filters.get('cc'):
            filters['cc'] = filters['cc'].lower()
            
        self.logger.debug('uri: %s' % uri)
        self.logger.debug('params: %s', json.dumps(filters))

        self.logger.info('searching...')

        body = self.session.get(uri, params=filters, verify=self.verify_ssl)
        self.logger.debug('status code: ' + str(body.status_code))

        if body.status_code >= 422:
            max_retries = RETRIES
            while max_retries > 0:
                self.logger.warn('{} found, retrying in {}s... {} tries remaining'.format(body.status_code, RETRY_SLEEP,
                                                                                          max_retries))
                sleep(RETRY_SLEEP)
                body = self.session.get(uri, params=filters, verify=self.verify_ssl)
                if body.status_code == 200:
                    break
                else:
                    max_retries -= 1

        if body.status_code > 299:
            self.logger.warning('request failed: %s' % str(body.status_code))
            raise SystemExit

        s = (int(body.headers['Content-Length']) / 1024 / 1024)
        self.logger.info('processing {0} megs'.format(s))

        ret = body.content
        if not ret.startswith('['):
            self.logger.info('trying to decompress...')
            # http://stackoverflow.com/a/2695575
            ret = base64.b64decode(ret)
            try:
                ret = zlib.decompress(ret)
            except zlib.error as e:
                # v2 gzip style
                ret = zlib.decompress(ret, 16+zlib.MAX_WBITS)

        if decode:
            self.logger.info('decoding...')
            ret = json.loads(ret)

            if type(ret) == dict and ret.get('data'):
                ret = ret['data']

            self.logger.info('sorting...')
            if sort_direction == 'DESC':
                ret = sorted(ret, key=lambda o: o[sort], reverse=True)
            else:
                ret = sorted(ret, key=lambda o: o[sort])

        self.logger.debug('returning..')
        return ret

    def submit(self, data):
        """
        Submit records to CIF

        :param data: a single dict or a list of dicts
        :return: list

        list
        [{"observable": "1.1.1.1", "confidence": "85", "tlp": "amber", "group": "everyone", "tags": ["zeus","botnet"],
        "provider": "me.com"}, {"observable": "1.1.1.1", "confidence": "85", "tlp": "amber", "group": "everyone",
        "tags": "malware", "provider": "me.com"}]
        """

        if type(data) == dict:
            data = [data]

        if type(data[0]) != dict:
            raise RuntimeError('submitted data must be a dictionary')

        data = json.dumps(data)

        # TODO - http://docs.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests
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
        """
        Ping the server to verify connectivity
        :return: str
        """
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

    def aggregate(self, data, field='observable', sort='confidence', sort_secondary='reporttime'):
        """
        aggregate data
        :param data:
        :param field:
        :param sort:
        :return:
        """
        x = set()
        rv = []
        for d in sorted(data, key=lambda x: x[sort], reverse=True):
            if d[field] not in x:
                x.add(d[field])
                rv.append(d)

        rv = sorted(rv, key=lambda x: x[sort_secondary])
        return rv


def main():

    p = ArgumentParser(
        description=textwrap.dedent('''\
        Example usage:

            $ cif -q 130.201.0.2
            $ cif -q 130.201.0.0/16
            $ cif -q 2001:4860:4860::8888
            $ cif -q example.com
            $ cif -q 'http://www.example.com'
            $ cif -q 'john@example.com'
            $ cif -q bf9d457bcd702fe836201df1b48c0bec

            $ cif --tags botnet,zeus -c 85
            $ cif --application vnc,ssh --asns 1234 --cc RU,US
            $ cif -q example.com --tags botnet,zeus -c 85 --limit 50

            $ cif --otype ipv4 --aggregate observable --today

            $ cif --feed --otype ipv4 -c 85 -f csv
            $ cif --feed --otype fqdn -c 95 --tags botnet -f csv
            $ cif --feed --otype url -c 75 --today -f csv
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='cif'
    )

    # options
    p.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="logging level: INFO")
    p.add_argument('-d', '--debug', dest='debug', action="store_true", help="logging level: DEBUG")
    p.add_argument('-V', '--version', action='version', version=VERSION)
    p.add_argument('--no-verify-ssl', action="store_true", default=False)
    p.add_argument('-R', '--remote', help="remote api location", default=REMOTE_ADDR)
    p.add_argument('-T', '--token', help="specify token [default %(default)s", default=TOKEN)
    p.add_argument('--timeout',  help='connection timeout [default: %(default)s]', default="300")
    p.add_argument('-C', '--config',  help="configuration file [default: %(default)s]",
                   default=os.path.expanduser("~/.cif.yml"))

    p.add_argument('--sortby', help='sort output [default: %(default)s]', default='lasttime')
    p.add_argument('--sortby-direction', help='sortby direction [default: %(default)s]', default='ASC')
    p.add_argument('-f', '--format', help="specify output format [default: %(default)s]", default="table", choices=FORMATS.keys())

    # actions
    p.add_argument('-p', '--ping', action="store_true", help="ping")
    p.add_argument('-s', '--submit', action="store_true", help="submit a JSON object")

    # flags
    p.add_argument('-l', '--limit', help="result limit", default=LIMIT)
    p.add_argument('-n', '--nolog', help='do not log the search', default=None, action="store_true")

    # filters
    p.add_argument('-q', "--query", help="specify a search")
    p.add_argument('--firsttime', help='specify filter based on firsttime timestmap (greater than, '
                                       'format: YYYY-MM-DDTHH:MM:SSZ)')
    p.add_argument('--lasttime', help='specify filter based on lasttime timestamp (less than, format: '
                                      'YYYY-MM-DDTHH:MM:SSZ)')
    p.add_argument('--reporttime', help='specify filter based on reporttime timestmap (greater than, format: '
                                        'YYYY-MM-DDTHH:MM:SSZ)')
    p.add_argument('--reporttimeend', help='specify filter based on reporttime timestmap (less than, format: '
                                           'YYYY-MM-DDTHH:MM:SSZ)')
    p.add_argument("--tags", help="filter for tags")
    p.add_argument('--description', help='filter on description')
    p.add_argument('--otype', help='filter by otype')
    p.add_argument("--cc", help="filter for countrycode")
    p.add_argument('-c', '--confidence', help="specify confidence")
    p.add_argument('--rdata', help='filter by rdata')
    p.add_argument('--provider', help='filter by provider')
    p.add_argument('--asn', help='filter by asn')
    p.add_argument('--tlp', help='filter by tlp')
    p.add_argument('--proxy', help="specify a proxy to use [default %(default)s]", default=PROXY)

    p.add_argument('--feed', action="store_true", help="generate a feed of data, meaning deduplicated and whitelisted")
    p.add_argument('--whitelist-limit', help="specify how many whitelist results to use when applying to --feeds "
                                             "[default %(default)s]", default=WHITELIST_LIMIT)
    p.add_argument('--whitelist-confidence', help='by confidence (greater-than or equal to) [default: %(default)s]',
                   default=WHITELIST_CONFIDENCE)

    p.add_argument('--last-day', action="store_true", help='auto-sets reporttime to 23 hours and 59 seconds ago '
                                                           '(current time UTC) and reporttime-end to "now"')
    p.add_argument('--last-hour', action='store_true', help='auto-sets reporttime to the beginning of the previous full'
                                                            ' hour and reporttime-end to end of previous full hour')
    p.add_argument('--days', help='filter results within last X days')
    p.add_argument('--today', help='auto-sets reporttime to today, 00:00:00Z (UTC)', action='store_true')

    p.add_argument('--aggregate', help="aggregate around a specific field (ie: observable)")

    p.add_argument('--fields', help="specify field list to display [default: %(default)s]", default=','.join(FIELDS))
    p.add_argument('--filename', help='specify output filename [default: STDOUT]')
    p.add_argument('--ttl', help='specify number of pings to send [default: %(default)s]', default=PINGS)
    p.add_argument('--group', help='filter by group(s) (everyone,group1,group2,...)')
    p.add_argument('--application', help='filter based on application field')
    p.add_argument('--id', help='specify an id to retrieve')

    # Process arguments
    args = p.parse_args()
    setup_logging(args)
    logger = logging.getLogger(__name__)

    # read in the config
    config_opts = read_config(args)
    cmd_options = vars(args)

    # check the config against the arguments
    for v in cmd_options:
        if cmd_options[v] is None:
            cmd_options[v] = config_opts.get(v)

        if v == 'remote':
            if cmd_options[v] != REMOTE_ADDR_DEFAULT:
                continue
            else:
                cmd_options[v] = config_opts.get('remote', REMOTE_ADDR_DEFAULT)

    options = cmd_options
    if not options.get('token'):
        raise RuntimeError('missing --token')

    verify_ssl = True
    if config_opts.get('no_verify_ssl') or options.get('no_verify_ssl'):
        verify_ssl = False

    cli = Client(options['token'], remote=options['remote'], proxy=options.get('proxy'), verify_ssl=verify_ssl)

    if(options.get('query') or options.get('tags') or options.get('cc') or options.get('rdata') or options.get(
                'otype') or options.get('provider') or options.get('asn') or options.get('description')):
        filters = {}
        if options.get('query'):
            filters['observable'] = options['query']
        if options.get('cc'):
            filters['cc'] = options['cc']

        if options.get('tags'):
            filters['tags'] = options['tags']

        if options.get('description'):
            filters['description'] = options['description']

        if options.get('confidence'):
            filters['confidence'] = options['confidence']
        else:
            if options.get('feed'):
                filters['confidence'] = FEED_CONFIDENCE

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

        if options.get('tlp'):
            filters['tlp'] = options['tlp']

        if options.get('group'):
            filters['group'] = options['group']

        if options.get('application'):
            filters['application'] = options['application']

        if options.get('id'):
            filters['id'] = options['id']

        # needs to be MEG'd out.
        if options.get('last_day'):
            now = arrow.utcnow()
            filters['reporttimeend'] = '{0}Z'.format(now.format('YYYY-MM-DDTHH:mm:ss'))
            now = now.replace(days=-1)
            filters['reporttime'] = '{0}Z'.format(now.format('YYYY-MM-DDTHH:mm:ss'))
        elif options.get('last_hour'):
            now = arrow.utcnow()
            filters['reporttimeend'] = '{0}Z'.format(now.format('YYYY-MM-DDTHH:mm:ss'))
            now = now.replace(hours=-1)
            filters['reporttime'] = '{0}Z'.format(now.format('YYYY-MM-DDTHH:mm:ss'))
        elif options.get('today'):
            now = arrow.utcnow()
            filters['reporttime'] = '{0}Z'.format(now.format('YYYY-MM-DDT00:00:00'))

        if options.get('days'):
            now = arrow.utcnow()
            filters['reporttimeend'] = '{0}Z'.format(now.format('YYYY-MM-DDTHH:mm:ss'))
            now = now.replace(days=-int(options['days']))
            filters['reporttime'] = '{0}Z'.format(now.format('YYYY-MM-DDTHH:mm:ss'))

        DAYS=30

        if options.get('feed'):
            if options['limit'] == LIMIT:
                options['limit'] = FEED_LIMIT

            if not options.get('days'):
                now = arrow.utcnow()
                filters['reporttimeend'] = '{0}Z'.format(now.format('YYYY-MM-DDTHH:mm:ss'))
                now = now.replace(days=-DAYS)
                filters['reporttime'] = '{0}Z'.format(now.format('YYYY-MM-DDTHH:mm:ss'))

        ret = cli.search(limit=options['limit'], nolog=options['nolog'], filters=filters, sort=options['sortby'],
                         sort_direction=options['sortby_direction'])

        number_returned = len(ret)

        logger.info('returned: {0} records'.format(number_returned))

        if options.get('aggregate'):
            ret = cli.aggregate(ret, field=options['aggregate'])

        if options.get('feed'):
            wl_filters = copy.deepcopy(filters)
            wl_filters['tags'] = 'whitelist'
            wl_filters['confidence'] = args.whitelist_confidence

            now = arrow.utcnow()
            now = now.replace(days=-DAYS)
            wl_filters['reporttime'] = '{0}Z'.format(now.format('YYYY-MM-DDTHH:mm:ss'))

            wl = cli.search(limit=options['whitelist_limit'], nolog=True, filters=wl_filters)

            f = feed_factory(options['otype'])

            ret = cli.aggregate(ret)

            if len(ret) != number_returned:
                logger.info('aggregation removed: {0} records'.format(number_returned - len(ret)))

            ret = f().process(ret, wl)

        f = format_factory(options['format'])
        if f is None:
            raise SystemError('{0} format not supported, maybe missing a dependency.'.format(options['format']))

        try:
            if len(ret) >= 1:
                ret = f(ret, cols=options['fields'].split(','))
                if args.filename:
                    with open(args.filename, 'w') as F:
                        F.write(str(ret))
                else:
                    signal(SIGPIPE, SIG_DFL)
                    print(ret)
            else:
                logger.info("no results found...")
        except AttributeError as e:
            logger.exception(e)

    elif options.get('ping'):
        for num in range(0, args.ttl):
            ret = cli.ping()
            print("roundtrip: %s ms" % ret)
            select.select([], [], [], 1)
    elif options.get('submit'):

        if not sys.stdin.isatty():
            stdin = sys.stdin.read()
        else:
            logger.error("No data passed via STDIN")
            raise SystemExit

        try:
            data = json.loads(stdin)
            try:
                ret = cli.submit(data)
                print('submitted: {0}'.format(ret))
            except Exception as e:
                logger.error(e)
                raise SystemExit
        except Exception as e:
            logger.error(e)
            raise SystemExit
    else:
        logger.warning('operation not supported')
        p.print_help()
        raise SystemExit

if __name__ == "__main__":
    main()
