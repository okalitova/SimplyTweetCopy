from flask import session
from app import app, redis_store
import json
import time
from app.images import ImagesStorage
from PIL import Image


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
            redis_store.set(username, json.dumps({"followings": [], "posts": []}))
        session["userid"] = userid
        session["email"] = email
        session["username"] = username
        app.logger.debug("New current user %s with email %s and userid %s",
                         session["username"],
                         session["email"],
                         session["userid"])

    def remove_current_user():
        session.clear()
        app.logger.debug("Current user removed")

    def add_post(username, text, image):
        image_key = None
        if image is not None:
            app.logger.debug("Image: %s", image)
            images_storage = ImagesStorage()
            image_key = images_storage.put_image(image)
            app.logger.debug("Image key: %s", image_key)
        user_info_json = UserInfo.get_user_info(username)
        user_info_json["posts"].append({"text": text, "timestamp": time.time(), "image_key": image_key})
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
        app.logger.debug("All followings posts: %s", users_posts)
        merged_posts_text = []
        while True:
            mmax = 0
            argmax = -1
            for i, user_posts in enumerate(users_posts):
                if pointers[i] < len(user_posts) and mmax < float(user_posts[pointers[i]]["timestamp"]):
                    mmax = float(user_posts[pointers[i]]["timestamp"])
                    argmax = i
            if argmax == -1:
                break
            app.logger.debug("Coolest ts: %s", users_posts[argmax][pointers[argmax]]["text"])
            merged_posts_text.append(users_posts[argmax][pointers[argmax]]["text"])
            pointers[argmax] += 1
        return merged_posts_text

    def add_following(current_user, user_to_follow):
        user_info_json = UserInfo.get_user_info(current_user)
        user_info_json["followings"].append(user_to_follow)
        app.logger.debug("New user info: %s", user_info_json)
        user_info_str = json.dumps(user_info_json)
        redis_store.set(current_user, user_info_str)
        app.logger.debug("New following: %s", UserInfo.get_followings(current_user))

    def get_user_info(username):
        app.logger.debug("Getting user info for %s", username)
        user_info_str = redis_store.get(username).decode("utf-8")
        app.logger.debug("User info str: %s", user_info_str)
        user_info_json = json.loads(user_info_str)
        app.logger.debug("User info json: %s", user_info_json)
        return user_info_json

    def get_followings(username):
        user_info_json = UserInfo.get_user_info(username)
        app.logger.debug("User info json: %s", user_info_json)
        user_followings = set(user_info_json["followings"])
        app.logger.debug("Followings: %s", user_followings)
        return user_followings
