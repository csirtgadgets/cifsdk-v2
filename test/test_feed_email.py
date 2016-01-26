import pytest


from cifsdk.feed.email import Email

data = [
    {
        'observable': 'barbtrave@usamedia.tv',
        'tags': 'phishing',
    },
    {
        'observable': 'bad@example.com',
        'tags': 'malware',
    },
]

whitelist = [
    {
        'observable': 'bad@example.com',
    }
]


def test_feed_email_whitelist():
    x = Email()

    y = x.process(data, whitelist)

    s = set()

    for xx in x.process(data, whitelist):
        s.add(xx['observable'])

    assert 'bad@example.com' not in s
    assert 'barbtrave@usamedia.tv' in s