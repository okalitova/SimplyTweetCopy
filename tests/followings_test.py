import unittest
from unittest.mock import patch

from app.followings import get_followings
from tests.mock_redis import MockRedis


@patch("app.user_info.redis_store", MockRedis)
class FollowingsTest(unittest.TestCase):
    def test_get_followings(self):
        followings = get_followings(MockRedis.TEST_USER_1)
        self.assertEqual(followings, set(MockRedis.TEST_USER_1_FOLLOWINGS))
