import unittest
from unittest.mock import patch

from app.posts import add_post,\
                      get_followings_posts,\
                      to_posts_to_show,\
                      get_posts
from tests.mock_redis import MockRedis


class PostsTest(unittest.TestCase):

    def tearDown(self):
        MockRedis.to_initial_state()

    @patch("app.user_info.redis_store", MockRedis)
    @patch("app.posts.redis_store", MockRedis)
    def test_add_post(self):
        post_text = "post text"
        post_image = None
        add_post(MockRedis.USERID_1,
                 post_text,
                 post_image)
        posts = get_posts(MockRedis.USERID_1)
        self.assertEqual(posts[0]["text"], post_text)

    @patch("app.user_info.redis_store", MockRedis)
    @patch("app.posts.redis_store", MockRedis)
    def test_get_followings_posts(self):
        posts = get_followings_posts(MockRedis.TEST_USER_1_FOLLOWINGS)
        self.assertEqual(posts,
                         to_posts_to_show(MockRedis
                                          .TEST_USER_1_FOLLOWINGS_POSTS))
