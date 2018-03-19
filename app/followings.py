import json

from app import redis_store
from app.user_info import UserInfo


def add_following(current_userid, to_follow_userid):
    user_info_json = UserInfo.get_user_info(current_userid)
    user_info_json["followings"]\
        .append({"userid": to_follow_userid,
                 "email": UserInfo.get_user_email(to_follow_userid)})
    user_info_str = json.dumps(user_info_json)
    redis_store.set(current_userid, user_info_str)


def delete_following(current_userid, to_unfollow_userid):
    user_info_json = UserInfo.get_user_info(current_userid)
    unfollow_user_index = -1
    for i, following in enumerate(user_info_json["followings"]):
        if following["userid"] == to_unfollow_userid:
            unfollow_user_index = i
            break
    if unfollow_user_index == -1:
        raise ValueError("Cannot unfollow not followed user.")
    else:
        del user_info_json["followings"][unfollow_user_index]
        user_info_str = json.dumps(user_info_json)
        redis_store.set(current_userid, user_info_str)


def get_followings(userid):
    user_info_json = UserInfo.get_user_info(userid)
    user_followings = user_info_json["followings"]
    return user_followings


def get_followings_ids(userid):
    followings = get_followings(userid)
    followings_ids = []
    for following in followings:
        followings_ids.append(following["userid"])
    return followings_ids
