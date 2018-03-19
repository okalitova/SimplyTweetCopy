import json


class MockRedis():
    USERID_1 = "test_user_1"
    EMAIL_1 = "a@b.c"
    USER_1 = {"userid": USERID_1,
              "email": EMAIL_1}
    USERID_2 = "test_user_2"
    EMAIL_2 = "test@gmail.com"
    USER_2 = {"userid": USERID_2,
              "email": EMAIL_2}
    USERID_3 = "test_user_3"
    EMAIL_3 = "lets@yamdex.ru"
    USER_3 = {"userid": USERID_3,
              "email": EMAIL_3}
    USERID_4 = "test_user_4"
    EMAIL_4 = "vot@dss.phystech.edu"
    USER_4 = {"userid": USERID_4,
              "email": EMAIL_4}
    POST_1 = {"email": EMAIL_1,
              "text": "post #1",
              "timestamp": 1.,
              "image_key": None}
    POST_2 = {"email": EMAIL_2,
              "text": "post #2",
              "timestamp": 3.2,
              "image_key": None}
    POST_3 = {"email": EMAIL_2,
              "text": "post #3",
              "timestamp": 4,
              "image_key": None}
    POST_33 = {"email": EMAIL_3,
               "text": "post #33",
               "timestamp": 4,
               "image_key": None}
    POST_4 = {"email": EMAIL_4,
              "text": "post #4",
              "timestamp": 15210978,
              "image_key": None}
    POST_5 = {"email": EMAIL_3,
              "text": "post #5",
              "timestamp": 15210979,
              "image_key": None}
    POST_6 = {"email": EMAIL_2,
              "text": "post #6",
              "timestamp": 16456831,
              "image_key": None}
    DATA = {USERID_1:
            json.dumps({"email": EMAIL_1,
                        "followings": [USER_2, USER_3, USER_4],
                        "posts": [POST_1]})
            .encode("utf-8"),
            USERID_2:
            json.dumps({"email": EMAIL_2,
                        "followings": [USER_4, USER_1],
                        "posts": [POST_2, POST_3, POST_6]})
            .encode("utf-8"),
            USERID_3:
            json.dumps({"email": EMAIL_3,
                        "followings": [USER_1, USER_4],
                        "posts": [POST_33, POST_5]})
            .encode("utf-8"),
            USERID_4:
            json.dumps({"email": EMAIL_4,
                        "followings": [],
                        "posts": [POST_4]})
            .encode("utf-8"),
            EMAIL_1: USERID_1.encode("utf-8"),
            EMAIL_2: USERID_2.encode("utf-8"),
            EMAIL_3: USERID_3.encode("utf-8"),
            EMAIL_4: USERID_4.encode("utf-8")}

    TEST_USER_1_FOLLOWINGS_POSTS = [POST_6,
                                    POST_5,
                                    POST_4,
                                    POST_3,
                                    POST_33,
                                    POST_2]

    TEST_USER_1_FOLLOWINGS = [USERID_2, USERID_3, USERID_4]

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
