import unittest
from unittest.mock import patch
from app.login import validate_iss, set_user_info


class LoginTest(unittest.TestCase):
    USER_ID = "user_id"
    EMAIL = "test-email.first@gmail.com"
    USERNAME = "test-email.first"
    VALID_IDINFO_1 = {"iss": "accounts.google.com",
                      "sub": USER_ID,
                      "email": EMAIL}

    VALID_IDINFO_2 = {"iss": "https://accounts.google.com",
                      "sub": USER_ID,
                      "email": EMAIL}

    INVALID_IDINFO = {"iss": "invalid_iss",
                      "sub": USER_ID,
                      "email": EMAIL}

    def test_validate_iss_if_valid(self):
        validate_iss(LoginTest.VALID_IDINFO_1)
        validate_iss(LoginTest.VALID_IDINFO_2)

    def test_validate_iss_if_invalid(self):
        with self.assertRaises(ValueError) as context:
            validate_iss(LoginTest.INVALID_IDINFO)
        self.assertTrue("Wrong issuer." in str(context.exception))

    @patch("app.login.UserInfo")
    def test_set_user_info(self, mock_user_info):
        set_user_info(LoginTest.VALID_IDINFO_1)
        mock_user_info.add_current_user.assert_called_with(LoginTest.USER_ID,
                                                           LoginTest.EMAIL,
                                                           LoginTest.USERNAME)
