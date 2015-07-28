from cifsdk.format.cifjson import Json


def test_format_json():
    data = [{
            'observable': "example.com",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z'
            },
            {
            'observable': "example.com",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z'
            },
            {
            'observable': "example.com",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z'
            }]

    print(Json(data))
    assert Json(data)

if __name__ == '__main__':
    test_format_json()
