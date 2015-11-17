import py.test
from cifsdk.client import Client


def test_client():
    cli = Client(token=1234, remote='https://localhost2:8443', verify_ssl=False)

    assert cli.verify_ssl is False
    assert cli.remote == 'https://localhost2:8443','remote-mismatch'
    assert cli.token == '1234', 'token mismatch'
