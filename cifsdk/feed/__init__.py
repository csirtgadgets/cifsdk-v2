from cifsdk.feed.fqdn import Fqdn
from cifsdk.feed.ipv4 import Ipv4
from cifsdk.feed.ipv6 import Ipv6
from cifsdk.feed.url import Url
from cifsdk.feed.email import Email
from cifsdk.feed.md5 import Md5
from cifsdk.feed.sha1 import Sha1
from cifsdk.feed.sha256 import Sha256
from cifsdk.feed.sha512 import Sha512


plugins = {
    'ipv4': Ipv4,
    'ipv6': Ipv6,
    'fqdn': Fqdn,
    'url': Url,
    'email': Email,
    'md5': Md5,
    'sha1': Sha1,
    'sha256': Sha256,
    'sha512': Sha512
}


# http://stackoverflow.com/a/456747
def factory(name):
    if name in plugins:
        return plugins[name]
    else:
        return None


def tag_contains_whitelist(data):
    for d in data:
        if d == 'whitelist':
            return True
