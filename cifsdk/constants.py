import os

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'

REMOTE_ADDR = 'https://localhost'
REMOTE_ADDR = os.environ.get('CIF_REMOTE_ADDR', REMOTE_ADDR)

LIMIT = 500
LIMIT = os.environ.get('CIF_LIMIT', LIMIT)

FEED_CONFIDENCE = 65
FEED_CONFIDENCE = os.environ.get('CIF_FEED_CONFIDENCE', FEED_CONFIDENCE)

WHITELIST_LIMIT = 25000
WHITELIST_LIMIT = os.environ.get('CIF_WHITELIST_LIMIT', WHITELIST_LIMIT)

PROXY = os.environ.get('CIF_PROXY')