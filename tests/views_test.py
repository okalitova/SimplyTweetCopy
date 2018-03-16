import unittest
from unittest.mock import patch

from app import app
from app.posts import to_posts_to_show
from tests.mock_redis import MockRedis


class ViewsTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.test_client = app.test_client()

    def test_main_page(self):
        rv = self.test_client.get("/")
        self.assertEqual(rv.status_code, 200)

    def test_login_page(self):
        rv = self.test_client.get("/login")
        self.assertEqual(rv.status_code, 200)

    @patch("app.views.UserInfo")
    def test_profile(self, mock_user_info):
        rv = self.test_client.get("/logout", follow_redirects=True)
        mock_user_info.remove_current_user.assert_called_with()
        self.assertEqual(rv.status_code, 200)

    @patch("app.views.UserInfo")
    def test_user_page_if_not_exist(self, mock_user_info):
        mock_user_info.check_user_exists.return_value = False
        rv = self.test_client.get("/non_existing_user")
        self.assertEqual(rv.status_code, 404)

    @patch("app.views.get_followings")
    @patch("app.views.get_posts_to_show")
    @patch("app.views.UserInfo")
    def test_user_page_if_exists_current_user_page(self,
                                                   mock_user_info,
                                                   mock_get_posts_to_show,
                                                   mock_get_followings):
        mock_user_info.get_current_user_username.return_value = \
            "current_user_username"
        mock_user_info.check_user_exists.return_value = True
        mock_get_posts_to_show.return_value = \
            to_posts_to_show([MockRedis.TEST_POST_1, MockRedis.TEST_POST_2])
        mock_get_followings.return_value = [MockRedis.TEST_USER_2]

        rv = self.test_client.get("/current_user_username")
        
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b"tweet_button" in rv.data)
