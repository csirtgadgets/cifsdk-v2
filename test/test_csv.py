from cifsdk.format.cifcsv import Csv


def test_format_csv():
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
    assert str(Csv(data))