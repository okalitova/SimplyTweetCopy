import json


class MockRedis():
    TEST_USER_1 = "test_user_1"
    TEST_USER_2 = "test_user_2"
    TEST_USER_3 = "test_user_3"
    TEST_USER_4 = "test_user_4"
    TEST_POST_1 = {"text": "post #1", "timestamp": 1., "image_key": None}
    TEST_POST_2 = {"text": "post #2", "timestamp": 3.2, "image_key": None}
    TEST_POST_3 = {"text": "post #3", "timestamp": 4, "image_key": None}
    TEST_POST_33 = {"text": "post #33", "timestamp": 4, "image_key": None}
    TEST_POST_4 = {"text": "post #4", "timestamp": 15210978, "image_key": None}
    TEST_POST_5 = {"text": "post #5", "timestamp": 15210979, "image_key": None}
    TEST_POST_6 = {"text": "post #6", "timestamp": 16456831, "image_key": None}
    DATA = {TEST_USER_1:
            json.dumps({"followings": [TEST_USER_2, TEST_USER_3, TEST_USER_4],
                        "posts": [TEST_POST_1]})
            .encode("utf-8"),
            TEST_USER_2:
            json.dumps({"followings": [TEST_USER_4, TEST_USER_1],
                        "posts": [TEST_POST_2, TEST_POST_3, TEST_POST_6]})
            .encode("utf-8"),
            TEST_USER_3:
            json.dumps({"followings": [TEST_USER_1, TEST_USER_4],
                        "posts": [TEST_POST_33, TEST_POST_5]})
            .encode("utf-8"),
            TEST_USER_4:
            json.dumps({"followings": [],
                        "posts": [TEST_POST_4]})
            .encode("utf-8")}

    TEST_USER_1_FOLLOWINGS_POSTS = [TEST_POST_6,
                                    TEST_POST_5,
                                    TEST_POST_4,
                                    TEST_POST_3,
                                    TEST_POST_33,
                                    TEST_POST_2]

    TEST_USER_1_FOLLOWINGS = [TEST_USER_2, TEST_USER_3, TEST_USER_4]

    INITIAL_DATA = DATA.copy()

    def set(key, value):
        MockRedis.DATA[key] = value.encode("utf-8")

    def get(key):
        if key in MockRedis.DATA:
            return MockRedis.DATA[key]
        else:
            return None

    def to_initial_state():
        MockRedis.DATA = MockRedis.INITIAL_DATA.copy()
