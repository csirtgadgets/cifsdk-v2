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
from pprint import pprint

CONFIDENCE = 50
MONTHS = 12
LIMIT = 5000


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

    body = {
        'query': {
            'filtered': {
                'filter': {
                    'and': [
                        {
                            'range': {
                                'confidence': {'lt': args.confidence}
                            }
                        }
                    ]
                }
            }
        }
    }

    monthlies = es.indices.get_aliases(index='{}-*.*'.format(args.index_prefix)).keys()
    to_cull = {}
    for m in monthlies:
        match = re.search(r"^cif\.observables-(\d{4}\.\d{2})$", m)
        if match.group(1) < end_month:
            to_cull['{}-{}'.format(args.index_prefix, match.group(1))] = '{}-{}'.format(args.index_prefix,
                                                                                        match.group(1))

    # https://www.elastic.co/guide/en/elasticsearch/reference/1.4/docs-delete-by-query.html
    # http://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.delete_by_query
    # http://stackoverflow.com/questions/26808239/elasticsearch-python-api-delete-documents-by-query

    for c in to_cull:
        logger.info('culling: {}'.format(c))
        if not args.dry_run:
            rv = helpers.scan(
                es,
                index=c,
                query=body,
                scroll='5m',
                size=LIMIT,
            )

            for r in rv:
                pprint(r)

            # rv = es.delete_by_query(
            #     index=c,
            #     body=body,
            #     wait_for_completion=True
            #
            # )
            # pprint(rv)
            # es.indices.optimize(index=to_cull[c])

if __name__ == "__main__":
    main()
