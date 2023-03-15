# Rumor Detection and Analysis on Tweets

## Overview
This is a data pipeline to detect and analyze rumors in tweets. The pipeline includes data scraping using the Tweepy API, data preprocessing, feature engineering, and rumor classification using [BERT](https://pytorch.org/hub/huggingface_pytorch-transformers/) model from PyTorch and ensemble classifier [XGBoost](https://xgboost.readthedocs.io/en/stable/). The pipeline was trained, validated and tested on 35k+ data with 60% labeled, achieving a 90% F1 score in the test dataset and ranking in the top 25% of the Kaggle competition. Additionally, we conducted rumor detection on 10k COVID-related tweets and analyzed topic trends, hashtags, sentiment, and user traits using Python.

## Contributors
Cheng, A., Qu, X., Zhang, K.

## Usage
- Run pget_tweet_data.py](https://github.com/AllisonXY/rumor-detection-on-tweets/blob/master/Get_Tweet_Data/get_tweet_data.py) to scrape tweets using the Tweepy API.
- Run [preprocess_data.py](https://github.com/AllisonXY/rumor-detection-on-tweets/blob/master/Data_preprocess/preprocess.py) to preprocess the scraped data.
- Run [Bert_XGBOOST.ipynb](https://github.com/AllisonXY/rumor-detection-on-tweets/blob/master/Models/Bert_XGBOOST.ipynb) to extract contextual representation of preprocessed data from BERT model and make rumor classification using XGBoost.
- Run [rumor_analysis.ipynb](https://github.com/AllisonXY/rumor-detection-on-tweets/blob/master/Rumor_analysis/rumor_analysis.ipynb) to analyze topic trends, hashtags, sentiment, and user traits in rumor VS non-rumor covid-related tweets. 


