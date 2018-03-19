import unittest
from unittest.mock import patch

from app import app
from tests.mock_redis import MockRedis


class ViewsTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.test_client = app.test_client()
        # user info mock
        self.patcher_user_info_1 = patch("app.views.UserInfo")
        self.mock_user_info_1 = self.patcher_user_info_1.start()
        self.mock_user_info_1.get_current_user_userid.return_value = \
            MockRedis.USERID_2
        self.mock_user_info_1.check_user_exists.return_value = True
        # second user info mock
        self.patcher_user_info_2 = patch("app.renderers.UserInfo")
        self.mock_user_info_2 = self.patcher_user_info_2.start()
        self.mock_user_info_2.get_current_user_userid.return_value = \
            MockRedis.USERID_2
        self.mock_user_info_2.check_user_exists.return_value = True
        # posts mock
        self.patcher_get_posts_to_show_1 = patch("app.views.get_posts_to_show")
        self.mock_get_posts_to_show_1 = \
            self.patcher_get_posts_to_show_1.start()
        self.mock_get_posts_to_show_1.return_value = [MockRedis.POST_1]
        # second posts mock
        self.patcher_get_posts_to_show_2 = \
            patch("app.renderers.get_posts_to_show")
        self.mock_get_posts_to_show_2 = \
            self.patcher_get_posts_to_show_2.start()
        self.mock_get_posts_to_show_2.return_value = [MockRedis.POST_1]

    def tearDown(self):
        self.patcher_user_info_1.stop()
        self.patcher_user_info_2.stop()
        self.patcher_get_posts_to_show_1.stop()
        self.patcher_get_posts_to_show_2.stop()
        MockRedis.to_initial_state()

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
        rv = self.test_client.get("/" + MockRedis.USERID_2)

        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b"tweet_button" in rv.data)

    def test_user_page_if_exists_following_page(self):
        rv = self.test_client.get("/" + MockRedis.USERID_1)

        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b"unfollow" in rv.data)

    def test_user_page_if_exists_not_following_page(self):
        rv = self.test_client.get("/" + MockRedis.USERID_3)

        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b"follow" in rv.data)

    @patch("app.user_info.redis_store", MockRedis)
    @patch("app.followings.redis_store", MockRedis)
    @patch("app.views.FollowForm")
    def test_new_following(self, mock_follow_form):
        mock_follow_form.return_value.validate_on_submit.return_value = True

        rv = self.test_client.post("/followings/new/" + MockRedis.USERID_3,
                                   follow_redirects=True)

        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b"post #1" in rv.data)
