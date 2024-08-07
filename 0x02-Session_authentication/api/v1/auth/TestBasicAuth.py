import unittest
from unittest.mock import patch, MagicMock
from api.v1.auth.basic_auth import BasicAuth
from models.user import User


class TestBasicAuth(unittest.TestCase):

    def setUp(self):
        self.auth = BasicAuth()

    @patch('models.user.User.search')
    @patch('models.user.User.count')
    def test_user_object_from_credentials_valid_credentials(self, mock_count, mock_search):
        print("Running test_user_object_from_credentials_valid_credentials")

        # Mock User.count to return a specific value
        mock_count.return_value = 1

        # Create a mock user object with the expected email and password
        mock_user = MagicMock(spec=User)
        mock_user.email = "user@example.com"
        mock_user.is_valid_password.return_value = True

        # Set the return value of the search method to include the mock user
        mock_search.return_value = [mock_user]

        # Call the method with valid credentials
        user = self.auth.user_object_from_credentials(
            "user@example.com", "password")
        print(f"Returned user: {user}")

        # Assert that the returned user is the mock user
        self.assertEqual(user, mock_user)

    @patch('models.user.User.search')
    def test_user_object_from_credentials_invalid_password(self, mock_search):
        print("Running test_user_object_from_credentials_invalid_password")
        mock_user = MagicMock(spec=User)
        mock_user.email = "user@example.com"
        mock_user.is_valid_password.return_value = False
        mock_search.return_value = [mock_user]
        result = self.auth.user_object_from_credentials(
            "user@example.com", "wrong_password")
        print(f"Returned result for invalid password: {result}")
        self.assertIsNone(result)

    @patch('models.user.User.search')
    def test_user_object_from_credentials_no_user_found(self, mock_search):
        print("Running test_user_object_from_credentials_no_user_found")
        mock_search.return_value = []
        result = self.auth.user_object_from_credentials(
            "user@example.com", "password")
        print(f"Returned result for no user found: {result}")
        self.assertIsNone(result)

    def test_user_object_from_credentials_none_email(self):
        print("Running test_user_object_from_credentials_none_email")
        result = self.auth.user_object_from_credentials(None, "password")
        print(f"Returned result for none email: {result}")
        self.assertIsNone(result)

    def test_user_object_from_credentials_none_password(self):
        print("Running test_user_object_from_credentials_none_password")
        result = self.auth.user_object_from_credentials(
            "user@example.com", None)
        print(f"Returned result for none password: {result}")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
