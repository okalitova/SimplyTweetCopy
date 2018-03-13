import json

from app import redis_store
from app.user_info import UserInfo


def add_following(current_user, user_to_follow):
    user_info_json = UserInfo.get_user_info(current_user)
    user_info_json["followings"].append(user_to_follow)
    user_info_str = json.dumps(user_info_json)
    redis_store.set(current_user, user_info_str)


def get_followings(username):
    user_info_json = UserInfo.get_user_info(username)
    user_followings = set(user_info_json["followings"])
    return user_followings
