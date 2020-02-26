# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 18:17:48 2019

@author: Mohammed EL-KHOU
"""

import tweepy
from tweepy import OAuthHandler
import twitter

import pandas as pd
import numpy as np
from tqdm import tqdm
import csv

#-----------------------------------------------------------------------
# load our API credentials
#-----------------------------------------------------------------------
import sys
sys.path.append(".")
import config

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
# Construct the API instance
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# api = tweepy.API(auth)

print("[Start]")
num_tweets = 5000000
outfile = "output2.csv"

#-----------------------------------------------------------------------
# Handling the rate limit using cursors
#-----------------------------------------------------------------------
import time
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            # time.sleep(15 * 60) # will wait for 15 minutes each time it hits the rate limit.
            time.sleep(15)
            print('cpp =',cpp,'[RateLimitError]')
        except tweepy.TweepError:
            time.sleep(10)
            print('cpp =',cpp,'[TweepError]')
        except tweepy.error.TweepError:
            time.sleep(10)
            print('cpp =',cpp,'[error.TweepError]')
        except:
            time.sleep(10)
            continue


cpp = 0
bar = tqdm(num_tweets)
#-----------------------------------------------------------------------
# perform a search based on latitude and longitude
# twitter API docs: https://dev.twitter.com/rest/reference/get/search/tweets
with open(outfile, mode='a', newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["user", "date", "text"])
    for tweet in tweepy.Cursor(api.search, geocode="31.632791,-7.988639,500km", since="2018-11-01", encoding='utf-8').items(num_tweets):
        #-----------------------------------------------------------------------
        # We add criteria to ignore tweets of Morocco neighbors
        # which are Algeria, Mauritania, Spain, and Portugal by using the
        # country code of Morocco which is ‘MA’:
        #-----------------------------------------------------------------------
        if tweet.place and tweet.place.country_code != 'MA' :
            continue
        if not tweet.text:
            continue
        cpp+=1
        bar.update(1)
        # df = df.append({"user" :tweet.user.screen_name, "date" :tweet.created_at, "text":tweet.text.encode("utf-8")},ignore_index=True )
        # print(str('@')+tweet.user.screen_name, "::", tweet.created_at, "::", str(tweet.text))
        user = tweet.user.screen_name
        date = tweet.created_at
        try:
            text = "" + tweet.text
        except:
            text = tweet.text.encode("utf-8")
        
        writer.writerow({"user" :user, "date" :date, "text":text})
#-----------------------------------------------------------------------
# now write this row to our CSV file
#-----------------------------------------------------------------------
# print("written to %s" % outfile)
# df.to_csv(outfile, index=False, encoding='utf-8', )
# df.to_csv(outfile, index=False, encoding='utf-8', mode='a', header=False)
bar.close()
print('cpp =',cpp,'\n[DONE]')