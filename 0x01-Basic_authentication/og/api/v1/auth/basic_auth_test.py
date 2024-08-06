import unittest
from unittest.mock import patch
from api.v1.auth.basic_auth import BasicAuth
import binascii


class TestBasicAuth(unittest.TestCase):
    def setUp(self):
        self.auth = BasicAuth()

    def test_decode_base64_authorization_header_with_none(self):
        result = self.auth.decode_base64_authorization_header(None)
        self.assertIsNone(result)

    def test_decode_base64_authorization_header_with_non_string(self):
        result = self.auth.decode_base64_authorization_header(89)
        self.assertIsNone(result)

    def test_decode_base64_authorization_header_with_valid_base64(self):
        result = self.auth.decode_base64_authorization_header(
            "SG9sYmVydG9uIFNjaG9vbA==")
        self.assertEqual(result, "Holberton School")

    @patch('api.v1.auth.basic_auth.base64.b64decode')
    def test_decode_base64_authorization_header_with_invalid_base64(self, mock_b64decode):
        mock_b64decode.side_effect = binascii.Error
        result = self.auth.decode_base64_authorization_header("InvalidBase64")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
