import tweepy
import json
import os

consumer_key = "CUyrghrUUeMBEkIghCcjGshMd"
consumer_secret = "ZfZzXXuGbrMZg0YXuDHIbRYKNPObo7tkzKFk78Eu0ZTeTGMcVk"
access_key = "4063815493-4sgKdnSOup4kkBIaEoqBu7AwLEmw196W6EM6Dvo"
access_secret = "UQjqwzGoVjCaibbJvOIDukxp38nFV0LPqLCdmhQIATtvB"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

id = '499761826822123520'
path = os.getcwd() + '\Dev_data'
json_id = path + '\\' + id + '.json'
with open(json_id, "w") as fp:
    status = api.get_status(id)
    json.dump(status._json, fp)