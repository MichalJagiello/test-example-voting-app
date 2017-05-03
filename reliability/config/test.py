import unittest

from config import Config


class ConfigTestCase(unittest.TestCase):

    def test_config_from_test_file(self):
        c = Config('test_config.yml')
        self.assertEqual(c['TEST1'], 'a')
        self.assertEqual(c['TEST2'], 'b')
        self.assertEqual(c['TEST3'], 'c')

if __name__ == "__main__":
    unittest.main()
