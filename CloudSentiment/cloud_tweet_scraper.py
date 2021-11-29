import numpy as np
import pandas as pd
import tweepy
import requests
import time
import json

from google.cloud import storage
from datetime import date
from datetime import timedelta
from CloudSentiment.cloud_params import KEY_PATH, BUCKET_NAME

SEARCH_URL = "https://api.twitter.com/2/tweets/search/all"

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name, prefix="tweet_data")
    for blob in blobs:
        print(blob.name)



class TweetScraper(object):
    def __init__(self, start_date, end_date, topic):
        self.date = [end_date, start_date]
        #self.end_date = end_date
        self.topic = topic
        self.bearer_token = None
        self.consumer_key = None
        self.consumer_secret = None
        self.access_token = None
        self.token_secret = None
        self.data = None
        self.df = None

    def set_keys(self):
        with open(KEY_PATH, "r") as key_file:
            keys = json.load(key_file)
        self.bearer_token = keys['bearer_token']
        self.consumer_key = keys['consumer_key']
        self.consumer_secret = keys['consumer_secret']
        self.access_token = keys['access_token']
        self.token_secret = keys['token_secret']
     
    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "CryptoTrading699"
        return r

    def connect_to_endpoint(self, url, params):
        response = requests.request("GET", SEARCH_URL, auth=self.bearer_oauth, params=params)
        #print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()


    def get_tweets(self, api_response, max_results=51):
        list_tweets = []

        for i in range(0,max_results):
            text = api_response['data'][i]['text']
            list_tweets.append(text)
        return list_tweets 


    def get_tweets_ids(self, api_response, max_results=51):
        list_tweets_ids = []

        for i in range(0,max_results):
            ids = api_response['data'][i]['id']
            list_tweets_ids.append(ids)
        return list_tweets_ids


    def get_dates(self, tweet_date, max_results=51):
        list_dates = []

        for i in range(0,max_results):
            list_dates.append(tweet_date)
        return list_dates


    def get_topic(self, topic, max_results=51):
        list_topics = [topic for i in range(0,max_results)]
        return list_topics

    # retrieve a dictionary of tweets(max_results) for each date, for each topic
    def get_tweets_dict(self, max_results=50):
        dates = self.date
        topics = [self.topic]
        tweeter_data = {
            'tweet':[],
            'tweet_date':[],
            'topic':[],
            'tweet_id':[],
        }

        # loop through dates
        for tweet_date in dates:
            # loop through topics
            for topic in topics:
                query_params = {'query':topic ,"end_time": tweet_date, "max_results":max_results, "tweet.fields":"public_metrics"}
                json_response = self.connect_to_endpoint(SEARCH_URL, query_params)
                available_tweets= len(json_response['data'])-1 # get number of tweets returned by the request if 

                tweeter_data['tweet'] += self.get_tweets(json_response, max_results=available_tweets)
                tweeter_data['tweet_id'] += self.get_tweets_ids(json_response, max_results=available_tweets)
                tweeter_data['tweet_date'] += self.get_dates(tweet_date, max_results=available_tweets)
                tweeter_data['topic'] += self.get_topic(topic, max_results=available_tweets)

                time.sleep(5)

        self.data = tweeter_data
        self.df = pd.DataFrame(self.data)

    # clean tweet corpus


    def clean_df(self, column = "tweet"):
        df = self.df
        df_column = self.df[column]
        df_column = df_column.str.replace("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)",'') # clean tweet of tags, punctuation
        df_column = df_column.str.lower()
        df.loc[:,f'clean_{column}'] = df_column
        df["title"] = df[f'clean_{column}'].apply(lambda x: str(x).replace('\n','')) # remove newlines '\n' from stings

        self.df = df

    def save_df(self):

        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"tweet_data/{self.topic}_{self.date[0]}")
        blob.upload_from_string(self.df.to_csv(),"text/csv")
        return self.df

if __name__ == "__main__":
    #scraper = TweetScraper('2021-11-25T00:00:00.000Z',
    #                            "2021-11-26T00:00:00.000Z",
    #                            "economy")
    #scraper.set_keys()
    #scraper.get_tweets_dict()
    #scraper.clean_df()
    #scraper.save_df()
    #print(scraper.df.head())
    list_blobs(BUCKET_NAME)#+"/tweet_data")
