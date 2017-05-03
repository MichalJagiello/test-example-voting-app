import unittest

from client import SplashClient
from client.errors import ServerNotResponseError


class ClientTestCase(unittest.TestCase):

    def test_ping(self):
        self.assertRaises(ServerNotResponseError,
                          SplashClient,
                          'not/valid/url')

        self.assertRaises(ServerNotResponseError,
                          SplashClient,
                          'http://www.onet.pl/')

        SplashClient('http://192.168.99.100:8050')

    def test_render_html(self):
        sc = SplashClient('http://192.168.99.100:8050')

        sc.render_html('http://192.168.99.101:81/')


if __name__ == "__main__":
    unittest.main()
