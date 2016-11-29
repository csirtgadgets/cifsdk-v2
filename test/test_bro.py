# -*- coding: utf-8 -*-
from cifsdk.format.bro import Bro


def test_format_bro():
    data = [
        {
            'observable': "example.com",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z',
            'otype': 'fqdn'
        },
        {
            'observable': "http://example.com/1234.htm",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z',
            'otype': 'url',
        },
        {
            'observable': "https://example.com/1234.htm",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z',
            'otype': 'url',
        },
        {
            'observable': "192.168.1.1",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z',
            'otype': 'ipv4'
        },
        {
            'observable': 'http://www.example.com/test.php?Ã£ÆÃ¢ÆÃ£Â¢Ã¢â¬Ã¢Å¡Ã£ÆÃ¢âÃ£âÃ¢Â¤a0bf64c8ba',
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z',
            'otype': 'ipv4'
        }
    ]

    text = str(Bro(data))
    print(text)
    assert text

if __name__ == '__main__':
    test_format_bro()
