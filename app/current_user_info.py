import json
import time

from flask import session

from app import redis_store
from app.images import ImagesStorage


class UserInfo():
    def is_logged_in():
        return "userid" in session

    def get_current_user_username():
        if UserInfo.is_logged_in():
            return session["username"]

    def get_current_user_email():
        if UserInfo.is_logged_in():
            return session["email"]

    def check_user_exists(username):
        return redis_store.get(username) is not None

    def add_current_user(userid, email, username):
        if redis_store.get(username) is None:
            redis_store.set(username,
                            json.dumps({"followings": [], "posts": []}))
        session["userid"] = userid
        session["email"] = email
        session["username"] = username

    def remove_current_user():
        session.clear()

    def add_post(username, text, image):
        image_key = None
        if image is not None:
            images_storage = ImagesStorage()
            image_key = images_storage.put_image(image)
        user_info_json = UserInfo.get_user_info(username)
        user_info_json["posts"].append({"text": text,
                                        "timestamp": time.time(),
                                        "image_key": image_key})
        user_info_str = json.dumps(user_info_json)
        redis_store.set(username, user_info_str)

    def get_posts(username):
        user_info_json = UserInfo.get_user_info(username)
        user_posts = user_info_json["posts"]
        return user_posts[::-1]

    def get_followings_posts(usernames):
        pointers = [0 for _ in range(len(usernames))]
        users_posts = []
        for username in usernames:
            users_posts.append(UserInfo.get_posts_with_ts(username))
        merged_posts = []
        while True:
            mmax = 0
            argmax = -1
            for i, user_posts in enumerate(users_posts):
                if pointers[i] < len(user_posts) and\
                        mmax < float(user_posts[pointers[i]]["timestamp"]):
                    mmax = float(user_posts[pointers[i]]["timestamp"])
                    argmax = i
            if argmax == -1:
                break
            merged_posts.append(users_posts[argmax][pointers[argmax]])
            pointers[argmax] += 1
        return merged_posts

    def add_following(current_user, user_to_follow):
        user_info_json = UserInfo.get_user_info(current_user)
        user_info_json["followings"].append(user_to_follow)
        user_info_str = json.dumps(user_info_json)
        redis_store.set(current_user, user_info_str)

    def get_user_info(username):
        user_info_str = redis_store.get(username).decode("utf-8")
        user_info_json = json.loads(user_info_str)
        return user_info_json

    def get_followings(username):
        user_info_json = UserInfo.get_user_info(username)
        user_followings = set(user_info_json["followings"])
        return user_followings
