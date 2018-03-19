import unittest
from unittest.mock import patch

from app import app
from tests.mock_redis import MockRedis


class ViewsTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.test_client = app.test_client()
        # user info mock
        self.patcher_user_info = patch("app.views.UserInfo")
        self.mock_user_info = self.patcher_user_info.start()
        self.mock_user_info.get_current_user_userid.return_value = \
            MockRedis.TEST_USER_2
        self.mock_user_info.check_user_exists.return_value = True
        # posts mock
        self.patcher_get_posts_to_show = patch("app.views.get_posts_to_show")
        self.mock_get_posts_to_show = self.patcher_get_posts_to_show.start()
        self.mock_get_posts_to_show.return_value = [MockRedis.TEST_POST_1]
        # followings mock
        self.patcher_get_followings_ids = patch("app.views.get_followings_ids")
        self.mock_get_followings_ids = self.patcher_get_followings_ids.start()
        self.mock_get_followings_ids.return_value = [MockRedis.TEST_USER_4,
                                                     MockRedis.TEST_USER_1]

    def tearDown(self):
        self.patcher_user_info.stop()
        self.patcher_get_posts_to_show.stop()
        self.patcher_get_followings_ids.stop()

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

    def test_user_page_if_exists_current_user_page(self):
        rv = self.test_client.get("/" + MockRedis.TEST_USER_2)

        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b"tweet_button" in rv.data)

    def test_user_page_if_exists_following_page(self):
        rv = self.test_client.get("/" + MockRedis.TEST_USER_1)

        self.assertEqual(rv.status_code, 200)
        self.assertFalse(b"follow" in rv.data)

    def test_user_page_if_exists_not_following_page(self):
        rv = self.test_client.get("/" + MockRedis.TEST_USER_3)

        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b"follow" in rv.data)

    @patch("app.user_info.redis_store", MockRedis)
    def test_new_following(self):
        rv = self.test_client.post("/followings/" + MockRedis.TEST_USER_3)

        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b"post #1" in rv.data)
