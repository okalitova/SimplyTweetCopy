import unittest
from unittest.mock import patch

from app import app
from flask import session

from app.user_info import UserInfo
from tests.mock_redis import MockRedis


class UserInfoTest(unittest.TestCase):
    USER_ID = "logged_user_userid"
    USER_EMAIL = "logged_user_email@gmail.com"
    USER_USERNAME = "logged_user_username"

    def set_session(self):
        session["userid"] = UserInfoTest.USER_ID
        session["email"] = UserInfoTest.USER_EMAIL

    def test_is_logged_in_if_yes(self):
        with app.test_request_context():
            self.set_session()
            self.assertTrue(UserInfo.is_logged_in())

    def test_is_logged_in_if_no(self):
        with app.test_request_context():
            self.assertFalse(UserInfo.is_logged_in())

    def test_get_current_user_userid(self):
        with app.test_request_context():
            self.set_session()

            self.assertEqual(UserInfo.get_current_user_userid(),
                             UserInfoTest.USER_ID)

    def test_get_currrent_user_email(self):
        with app.test_request_context():
            self.set_session()

            self.assertEqual(UserInfo.get_current_user_email(),
                             UserInfoTest.USER_EMAIL)

    def test_remove_curret_user(self):
        with app.test_request_context():
            self.set_session()

            UserInfo.remove_current_user()

            self.assertEqual(len(session), 0)

    @patch("app.user_info.redis_store", MockRedis)
    def test_check_user_exists_if_no(self):
        self.assertFalse(UserInfo.
                         check_user_exists(UserInfoTest.USER_USERNAME))

    @patch("app.user_info.redis_store", MockRedis)
    def test_check_user_exists_if_yes(self):
        self.assertTrue(UserInfo.
                        check_user_exists(MockRedis.USERID_1))

    @patch("app.user_info.redis_store", MockRedis)
    def test_get_user_info(self):
        user_info = UserInfo.get_user_info(MockRedis.USERID_1)
        self.assertEqual(len(user_info["followings"]), 3)
        self.assertEqual(len(user_info["posts"]), 1)
