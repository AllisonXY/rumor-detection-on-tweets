import tweepy
import json
import os

consumer_key = "CUyrghrUUeMBEkIghCcjGshMd"
consumer_secret = "ZfZzXXuGbrMZg0YXuDHIbRYKNPObo7tkzKFk78Eu0ZTeTGMcVk"
access_key = "4063815493-4sgKdnSOup4kkBIaEoqBu7AwLEmw196W6EM6Dvo"
access_secret = "UQjqwzGoVjCaibbJvOIDukxp38nFV0LPqLCdmhQIATtvB"

# consumer_key = "Ozup2OAf8pHZhha38AELtzswf"
# consumer_secret = "T0QCvEWdUm2PakSKDsho9usdvaPWZsUB0hhB2XE1JwgwCGp7wV"
# access_key = "1252083222189498368-BZUECSVoWd6IDSWGnETwH4krVS3AHh"
# access_secret = "y9UNO50rhFndcMPy4S4cY5qLEcZdz6NygWyl8t0ZY7H8s"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

# train_data = []
# with open(r".\project-data\train.data.txt", "r") as f:
#     data_set = list(f)
#     for data in data_set:
#         id_sets= data.split(',')
#         for id in id_sets:
#             train_data.append(id.replace('\n', ''))


# path = os.getcwd() + '\Train_data'
# for id in train_data:
#     json_id = path + '\\' + id + '.json'
#     if os.path.exists(json_id) == False:
#             if api.lookup_statuses([id]) != []:
#                 with open(json_id, "w") as fp:
#                     status = api.get_status(id)
#                     json.dump(status._json, fp)


dev_data = []
with open(r".\project-data\dev.data.txt", "r") as f:
    data_set = list(f)
    for data in data_set:
        id_sets= data.split(',')
        for id in id_sets:
            dev_data.append(id.replace('\n', ''))

path = os.getcwd() + '\Dev_data'
for id in dev_data:
    json_id = path + '\\' + id + '.json'
    if os.path.exists(json_id) == False:
            if api.lookup_statuses([id]) != []:
                with open(json_id, "w") as fp:
                    status = api.get_status(id)
                    json.dump(status._json, fp)

covid_data = []
with open(r".\project-data\covid.data.txt", "r") as f:
    data_set = list(f)
    for data in data_set:
        id_sets= data.split(',')
        for id in id_sets:
            covid_data.append(id.replace('\n', ''))


path = os.getcwd() + '\Covid_data'
for id in covid_data:
    json_id = path + '\\' + id + '.json'
    if os.path.exists(json_id) == False:
            if api.lookup_statuses([id]) != []:
                with open(json_id, "w") as fp:
                    status = api.get_status(id)
                    json.dump(status._json, fp)