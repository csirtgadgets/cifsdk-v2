try:
    import elasticsearch  # 1.9.0
except ImportError:
    print('this module requires the elasticsearch library')
    raise ImportError

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import logging
import textwrap
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from elasticsearch import helpers
import re
from cifsdk import VERSION
from cifsdk.utils import setup_logging

CONFIDENCE = 0
MONTHS = 12

from pprint import pprint

def main():

    p = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ cif-es-reindex
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='cif-es-reindex'
    )

    # options
    p.add_argument("-v", "--verbose", action="store_true", help="logging level: INFO")
    p.add_argument('-d', '--debug', action="store_true", help="logging level: DEBUG")
    p.add_argument('-V', '--version', action='version', version=VERSION)
    p.add_argument('-m', '--months', help='how many months ago to cull [default %(default)s]', default=MONTHS)
    p.add_argument('-c', '--confidence', help='min confidence [default %(default)s]', default=CONFIDENCE)
    p.add_argument('--index-prefix', help='index prefix', default='cif.observables')
    p.add_argument('--dry-run', action="store_true", help='dry run, do not delete')
    p.add_argument('--nodes', default=['localhost:9200'])

    args = p.parse_args()
    setup_logging(args)
    logger = logging.getLogger(__name__)

    end_month = (datetime.today() - relativedelta(months=int(args.months)))
    end_month = end_month.strftime('%Y.%m')

    logger.info('month: {}'.format(end_month))

    es = Elasticsearch(args.nodes, timeout=120, max_retries=10, retry_on_timeout=True)

    # get list of dailies
    dailies = es.indices.get_aliases(index='{}-*.*.*'.format(args.index_prefix)).keys()  # daily indices only

    to_cull = {}
    for d in dailies:
        match = re.search(r"^cif\.observables\-((\d{4}\.\d{2})\.\d{2})$", d)
        if match.group(1):
            if match.group(1) < end_month:
                to_cull['{}-{}'.format(args.index_prefix, match.group(1))] = '{}-{}'.format(args.index_prefix, match.group(2))
    body = {
        'query': {
            'filtered': {
                'filter': {
                    'and': [
                        {
                            'range': {
                                'confidence': {'gte': args.confidence}
                            }
                        }
                    ]
                }
            }
        }
    }

    for c in to_cull:
        logger.info('culling: {}'.format(c))
        if not args.dry_run:
            s, f = helpers.reindex(es, c, target_index=to_cull[c], query=body, chunk_size=50000)
            logger.info('success: {}'.format(s))
            logger.info('failure: {}'.format(f))
            if f:
                logger.error('re-index failed: {}'.format(c))
                raise SystemError
            else:
                logger.info('closing index: {}'.format(c))
                es.indices.close(index=c)

        logger.info('optimizing: {}'.format(to_cull[c]))
        if not args.dry_run:
            es.indices.optimize(index=to_cull[c])



if __name__ == "__main__":
    main()
