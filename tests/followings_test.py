import unittest
from unittest.mock import patch

from app.followings import get_followings_ids
from tests.mock_redis import MockRedis


@patch("app.user_info.redis_store", MockRedis)
class FollowingsTest(unittest.TestCase):
    def test_get_followings_ids(self):
        followings_ids = get_followings_ids(MockRedis.USERID_1)
        self.assertEqual(followings_ids, MockRedis.TEST_USER_1_FOLLOWINGS)
