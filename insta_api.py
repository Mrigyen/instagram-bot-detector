from InstagramAPI import InstagramAPI
import loginkey
import requests
import re
import sys
import os


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


print("Attempting to log into Instagram API")
blockPrint()
api = InstagramAPI(loginkey.username, loginkey.password)
if api.login():
    enablePrint()
    print("Login Success")
else:
    enablePrint()
    print("Login Failure")


def get_user_id(username):
    r = requests.get("https://www.instagram.com/" + username + "/?__a=1")
    if r:
        r = r.json()["logging_page_id"]
        user_id = re.findall(r"[0-9]", r)
        user_id = ''.join(user_id)
        return user_id
    else:
        print("failed to find user")
        return None


def get_number_of_posts(user_id):
    api.getUsernameInfo(user_id)
    return api.LastJson["user"]["media_count"]


def get_number_of_people_they_follow(user_id):
    api.getUsernameInfo(user_id)
    return api.LastJson["user"]["following_count"]


def get_number_of_followers(user_id):
    api.getUsernameInfo(user_id)
    return api.LastJson["user"]["follower_count"]


def get_has_profile_picture(user_id):
    api.getUsernameInfo(user_id)
    return not api.LastJson["user"]["has_anonymous_profile_picture"]


def get_has_private_account(user_id):
    api.getUsernameInfo(user_id)
    return api.LastJson["user"]["is_private"]


def features(username):
    features = {}
    user_id = get_user_id(username)
    if user_id:
        # Add number of posts
        features["Number.of.posts"] = get_number_of_posts(user_id)

        # Add number of people they follow
        features["Number.of.people.they.follow"] = get_number_of_people_they_follow(user_id)

        # Add number of followers
        features["Number.of.followers"] = get_number_of_followers(user_id)

        # Add has profile pictures
        features["has_profile_picture"] = get_has_profile_picture(user_id)

        # Add has private account
        features["Private.account"] = get_has_private_account(user_id)

        # Add has number
        features["has_number"] = bool(re.search(r"\d", username))

        # Add has number at end
        features["has_number_at_end"] = bool(re.search(r"\d$", username))

        # Add alpha numeric ratio
        try:
            features["alpha_numeric_ratio"] = round(len(re.findall(r"[a-z]", username)) / len(username), 7)
        except ZeroDivisionError:
            features["alpha_numeric_ratio"] = 0.9011392054358974

        # Add following to followers ratio
        try:
            features["following_followers_ratio"] = round(
                    features["Number.of.people.they.follow"] / features["Number.of.followers"], 7)
        except ZeroDivisionError:
            features["following_followers_ratio"] = 6.4194135501560865

        # add following_posts_ratio
        try:
            features["following_posts_ratio"] = round(
                    features["Number.of.people.they.follow"] / features["Number.of.posts"], 7)
        except ZeroDivisionError:
            features["following_posts_ratio"] = 127.02637909977729

        # add followers_posts_ratio
        try:
            features["followers_posts_ratio"] = round(features["Number.of.followers"] / features["Number.of.posts"], 7)
        except ZeroDivisionError:
            features["followers_posts_ratio"] = 37.011870851559024

        return features
    else:
        return None
