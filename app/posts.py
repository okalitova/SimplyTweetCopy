from datetime import datetime
import json
import time

from app import redis_store
from app.images import ImagesStorage
from app.user_info import UserInfo


def add_post(userid, text, image):
    image_key = None
    if image is not None:
        images_storage = ImagesStorage()
        image_key = images_storage.put_image(image)
    user_info_json = UserInfo.get_user_info(userid)
    user_info_json["posts"].append({"text": text,
                                    "timestamp": time.time(),
                                    "image_key": image_key})
    user_info_str = json.dumps(user_info_json)
    redis_store.set(userid, user_info_str)


def delete_post(userid, timestamp):
    user_info_json = UserInfo.get_user_info(userid)
    to_delete_post_index = -1
    for i, post in enumerate(user_info_json["posts"]):
        print(post["timestamp"], timestamp)
        print(type(post["timestamp"]), type(timestamp))
        if post["timestamp"] == float(timestamp):
            to_delete_post_index = i
            break
    if to_delete_post_index == -1:
        raise ValueError("Delete post that is not posted.")
    else:
        del user_info_json["posts"][to_delete_post_index]
        user_info_str = json.dumps(user_info_json)
        redis_store.set(userid, user_info_str)


def get_posts(userid):
    user_info_json = UserInfo.get_user_info(userid)
    user_posts = user_info_json["posts"]
    user_posts_with_emails = []
    for post in user_posts:
        post["email"] = UserInfo.get_user_email(userid)
        user_posts_with_emails.append(post)
    return user_posts_with_emails[::-1]


def get_followings_posts(userids):
    pointers = [0 for _ in range(len(userids))]
    users_posts = []
    for userid in userids:
        users_posts.append(get_posts(userid))
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
    return to_posts_to_show(merged_posts)


def get_posts_to_show(userid):
    posts = get_posts(userid)
    return to_posts_to_show(posts)


def to_posts_to_show(posts):
    posts_to_show = []
    for post in posts:
        post["time"] = datetime.fromtimestamp(post["timestamp"])\
                                    .strftime('%Y-%m-%d %H:%M:%S')
        if "image_key" in post and post["image_key"] is not None:
            images_storage = ImagesStorage()
            image_link = images_storage.get_image(post["image_key"])
            post["image_link"] = image_link
        posts_to_show.append(post)
    return posts_to_show
