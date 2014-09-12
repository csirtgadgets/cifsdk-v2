import unittest
from cif.sdk.client import Client

class TestClient(unittest.TestCase):

    def setUp(self):
        self.cli = Client(token=1234,remote='https://localhost2:8443',
                          no_verify_ssl=1)
        
    def test_remote(self):
        self.assertEqual(self.cli.remote,'https://localhost2:8443','remote-mismatch')
    
    def test_verifyssl(self):
        self.assertEqual(self.cli.verify_ssl,0, 'verify-ssl mis-match')
        
    def test_token(self):
        self.assertEqual(self.cli.token,'1234','token-mismatch')

if __name__ == '__main__':
    unittest.main()
