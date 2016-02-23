STIX_ENABLED = True

try:
    from stix.core import STIXHeader
    from cifsdk.format.cif_stix import Stix
except ImportError:
    STIX_ENABLED = False

data = [
    {
        'observable': "example.com",
        'provider': "me.com",
        'tlp': "amber",
        'confidence': "85",
        'reporttime': '2015-01-01T00:00:00Z',
        'tags': ['botnet', 'malware']
    },
    {
        'observable': "example.com",
        'provider': "me.com",
        'tlp': "amber",
        'confidence': "85",
        'reporttime': '2015-01-01T00:00:00Z',
        'tags': ['botnet', 'malware']
    },
    {
        'observable': "example.com",
        'provider': "me.com",
        'tlp': "amber",
        'confidence': "85",
        'reporttime': '2015-01-01T00:00:00Z',
        'tags': ['botnet', 'malware']
    }
]


def test_stix():
    if STIX_ENABLED:
        d = Stix(data)
        assert len(str(d)) > 2
    else:
        print('STIX package not installed, skipping test')
