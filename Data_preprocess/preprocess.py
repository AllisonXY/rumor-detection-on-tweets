from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import logging
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from pandas import DataFrame
import csv #update
from json import JSONDecodeError  #update
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import nltk
from nltk.corpus import stopwords


punt_removal = nltk.RegexpTokenizer(r"\w+")
sid = SentimentIntensityAnalyzer()
sd_scale = StandardScaler()
mm_scale = MinMaxScaler()

train_path = '../Train_Data/'
train_data_list = '../project-data/train.data.txt'
train_label_list = '../project-data/train.label.txt'
train_pickle= '../project-data/train_df.pkl'

dev_path = '../Dev_Data/'
dev_data_list = '../project-data/dev.data.txt'
dev_label_list = '../project-data/dev.label.txt'
dev_pickle= '../project-data/dev_df.pkl'

test_path = '../Test_Data/'
test_data_list = '../project-data/test.data.txt'
test_pickle= '../project-data/test_df.pkl'

covid_path = '../Covid_Data/'
covid_data_list = '../project-data/covid.data.txt'
covid_pickle= '../project-data/covid_df.pkl'

# root_path= "D:\OneDrive\OneDrive - The University of Melbourne\COMP90042Project\{}"
# root_list_path= root_path.format("project-data\{}")

# train_path = root_path.format("Train_data\\")
# train_data_list = root_list_path.format("train.data.txt")
# train_label_list= root_list_path.format("train.label.txt")

# dev_path = root_path.format("Dev_data\\")
# dev_data_list = root_list_path.format("dev.data.txt")
# dev_label_list= root_list_path.format("dev.label.txt")

# test_path = root_path.format("Test_data\\")
# test_data_list = root_list_path.format("test.data.txt")

# # store orignal & clean text of source tweet for feature extraction  #update
# train_text=root_list_path.format("train_text.csv")
# dev_text=root_list_path.format("dev_text.csv")
# test_text=root_list_path.format("test_text.csv")


def extract_tweet(tweet_id, dir_path):  # extract source tweet
    try:
        with open(f'{dir_path}{tweet_id}.json') as json_file:
            data = json.load(json_file)
            return {'tweet_id': data['id'],
              'user_id' : data['user']['id'],
                  'followers_count' : data['user']['followers_count'],
                  'friends_count' : data['user']['friends_count'],
                  'listed_count' : data['user']['listed_count'],
                  'favourites_count' : data['user']['favourites_count'],
                  'verified' : 1 if data['user']['verified'] else 0,
                  'hastags' : data['entities']['hashtags'],
                  'text' : process_tweet_text(data['text']),            
                  'created_at' : data['created_at'],
                  'in_reply_to_status_id' : data['in_reply_to_status_id'],
                  'is_reply' : 1 if data['in_reply_to_status_id'] else 0,
                  'retweet_count': data['retweet_count'] ,   
                  'favorite_count': data['favorite_count']}
    except FileNotFoundError:
        logging.error(f"Target {tweet_id} not found")
    except JSONDecodeError:      # update
        logging.info(f"Target {tweet_id} is empty json file")
            
    
def extract_reply(tweet_id, dir_path):  # extract reply
    try:
        dir_path=dir_path.strip()
        tweet_id= tweet_id.strip()
        file_path= dir_path + tweet_id + ".json"
        with open(f'{dir_path}{tweet_id}.json') as json_file:
            data = json.load(json_file)
            return {'text' : process_tweet_text(data['text']),            
                          'created_at' : data['created_at']}
    except FileNotFoundError:
        logging.info(f"reply {tweet_id} not found")
    except JSONDecodeError:      # update
        logging.info(f"reply {tweet_id} is empty json file")

        
def process_tweet_text(text):
    text = text.lower()
    text = re.sub(r'https?:\/\/\S+', '', text)
    text = re.sub(r"www\.[a-z]?\.?(com)+|[a-z]+\.(com)", '', text)
    text = re.sub(r'@\w+', '', text)
    return text


"""
process list of replies into single dict
"""
def process_replies(replies, target_text):
    if len(replies) ==0:
        return {'reply_avg_sent' : 0,
              'reply_sent_trend': 0, 
              'reply_text': ''
              }
    reply_df = pd.DataFrame(replies)
    reply_df.sort_values('created_at', inplace=True)  #sort replies by chronological order
    reply_df['sent'] = reply_df.text.apply(lambda x: sid.polarity_scores(x)['compound']) 
    reply_df['text'] = reply_df.text.str.replace(target_text, ' ', regex=False)
    return {'reply_avg_sent' : reply_df.sent.mean(), #avg sentiment 
          'reply_sent_trend': 0, #is the reply sentiment up or down   #TODO why 0?
          'reply_text': ' '.join(list(reply_df.text)) 
          }

def clean_reply_text(tok, text):
    return ' '.join([word for word in tok.tokenize(text) if word not in stopwords.words('english')])

def process_data_file(list_file_path, tweet_path,label_file_path):  #update
    logging.basicConfig(filename=f'{list_file_path}process.log', level=logging.INFO, filemode='w', force=True)
    logging.info(f"start processing")
    all_labels, labels= [],[]  

    if label_file_path is not None:
        with open(label_file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                all_labels.append(row[0])  #all labels from label file

    with open(list_file_path, "r") as f:
        lines = list(f)
        target_tweets = [] #overall tweet dict
        for line in lines:  # each line= source+ replies
            tweets = line.split(',')
            reply_tweets = []
            for idx, tweet in enumerate(tweets): #['Python', 'Java']-> [(0, 'Python'), (1, 'Java')]
                if idx == 0: # source tweet
                    tweet_dict = extract_tweet(tweet.strip(), tweet_path) 
                    if tweet_dict is None:
                        logging.error('warning -- Missing a target tweet')
                        break
                else:
                    reply = extract_reply(tweet.strip(), tweet_path)
                    if reply is not None:
                        reply_tweets.append(reply)
            
            if tweet_dict is not None:    # 2nd for loop
                if label_file_path is not None:  #update
                    index= lines.index(line)
                    labels.append(all_labels[index])
                reply_dict = process_replies(reply_tweets, tweet_dict.get('text'))
                target_tweets.append({**tweet_dict, **reply_dict})
                
        tweet_df = pd.DataFrame(target_tweets)   # 1st for loop
        if label_file_path is not None:
            tweet_df['label'] = list(map((lambda x: 0 if x=='nonrumour' else 1), labels))
        tweet_df['clean_reply_text'] = tweet_df.reply_text.apply(lambda x: clean_reply_text(punt_removal, x))
        return tweet_df


train_df = process_data_file(train_data_list, train_path, train_label_list)
dev_df = process_data_file(dev_data_list, dev_path, dev_label_list)
test_df = process_data_file(test_data_list, test_path, None)  #y_test is []
covid_df = process_data_file(covid_data_list, covid_path, None)  #y_test is []
transform_candidate_cols = ['followers_count', 'friends_count', 'listed_count', 'favourites_count','retweet_count','favorite_count', 'reply_avg_sent']

train_df[transform_candidate_cols] = mm_scale.fit_transform(train_df[transform_candidate_cols])
dev_df[transform_candidate_cols] = mm_scale.transform(dev_df[transform_candidate_cols])
test_df[transform_candidate_cols] = mm_scale.transform(test_df[transform_candidate_cols])
covid_df[transform_candidate_cols] = mm_scale.transform(covid_df[transform_candidate_cols])

train_df.to_pickle(train_pickle, protocol=4)
dev_df.to_pickle(dev_pickle, protocol=4)
test_df.to_pickle(test_pickle, protocol=4)
covid_df.to_pickle(covid_pickle, protocol=4)
