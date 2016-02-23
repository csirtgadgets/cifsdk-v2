from cifsdk.format.cifsnort import Snort

import re
RULE_PATTERN = r'^alert (TCP|UDP|IP) (\S+) (\S+) -> ([^,]+)\s(\S+)\s\([^.]+\)'

def test_format_snort():
    data = [
        {
            'observable': "example.com",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z',
            'otype': 'fqdn',
            'tags': ['botnet']
        },
        {
            'observable': "http://example.com/1234.htm",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z',
            'otype': 'url',
            'tags': ['botnet']
        },
        {
            'observable': "https://example.com/1234.htm",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z',
            'otype': 'url',
            'tags': ['botnet']
        },
        {
            'observable': "192.168.1.1",
            'portlist': 8888,
            'protocol': 6,
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z',
            'otype': 'ipv4',
            'tags': ['botnet']
        }
    ]

    text = str(Snort(data))
    assert text
    assert re.findall(RULE_PATTERN, text)


if __name__ == '__main__':
    test_format_snort()
