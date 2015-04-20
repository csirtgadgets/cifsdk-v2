try:
    import re2 as re
except ImportError:
    import re

# based on some of the work by https://github.com/giovino

# http://stackoverflow.com/questions/499345/regular-expression-to-extract-url-from-an-html-link
# RE for URL extraction:
# http://daringfireball.net/2010/07/improved_regex_for_matching_urls
# http://daringfireball.net/misc/2010/07/url-matching-regex-test-data.text
# https://gist.github.com/uogbuji/705383
# GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([
# ^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

# re.compile(r'http.?://[a-z,/,\.,\d,\?,=,\-,\+,#,_,&,;,\,,:,@,%,]*', re.IGNORECASE).findall(xxx)
RE_URL = r'href=[\'"]?([^\'" >]+)'
REPLACE = ['=\n', "\t", "\r", '\\n']
REMOTE_DEFAULT = "http://localhost:5000"

from pprint import pprint

def extract_urls(msg):
    msg = msg.replace("=3D", '=')
    for x in REPLACE:
        msg = msg.replace(x, '')

    urls = re.findall(RE_URL, msg)
    links = set()
    for u in urls:
        u = u.rstrip("/")
        links.add(u)

    return links