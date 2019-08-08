from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import tweepy
import sys
from translate import Translator
import re
import matplotlib.pyplot as plt

#Enter your own details
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

s=raw_input("Enter twitter hanlder for different account separated by space")
account_list=s.split(' ');
def clean_tweet(tweet): 
        
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

if len(account_list) > 0:
  for target in account_list:
    print("Getting data for " + target)
    item = auth_api.get_user(target)
    name2=item.name
    print("Name: " + item.name)
    print("Screen Name: " + item.screen_name)
    print("Description: " + item.description)
    print("Tweets: " + str(item.statuses_count))
    print("Follows: " + str(item.friends_count))
    print("Followers: " + str(item.followers_count))

    tweets = item.statuses_count
    account_created_date = item.created_at
    delta = datetime.utcnow() - account_created_date
    account_age_days = delta.days
    print("Account age (in days): " + str(account_age_days))
    if account_age_days > 0:
        print("Average tweets per day: " + "%.2f"%(float(tweets)/float(account_age_days)))

    hashtags = []
    mentions = []
    tweet_count = 0
    end_date = datetime.utcnow() - timedelta(days=30)
    for status in Cursor(auth_api.user_timeline, id=target).items():
        tweet_count += 1
        if hasattr(status, "entities"):
            entities = status.entities
            if "hashtags" in entities:
              for ent in entities["hashtags"]:
                if ent is not None:
                  if "text" in ent:
                    hashtag = ent["text"]
                    if hashtag is not None:
                      hashtags.append(hashtag)
            if "user_mentions" in entities:
              for ent in entities["user_mentions"]:
                if ent is not None:
                  if "screen_name" in ent:
                    name = ent["screen_name"]
                    if name is not None:
                      mentions.append(name)
        if status.created_at < end_date:
            break
    print
    print("Most mentioned Twitter users:")
    for item, count in Counter(mentions).most_common(10):
        print(item + "\t" + str(count))
     
    print
    print("Most used hashtags:")
    for item, count in Counter(hashtags).most_common(10):
        print(item + "\t" + str(count))

    api = tweepy.API(auth) 
  
        # 100 tweets to be extracted 
    number_of_tweets=100
    tweets = api.user_timeline(screen_name=target) 
    tmp=[]
    tweets_for_csv = [tweet.text for tweet in tweets]
    for j in tweets_for_csv:
      j = j.encode("utf-8")      
      j=clean_tweet(j)
      tmp.append(j)  
    
    pos=0
    neg=0
    positive = open("positive_words.txt","r").readlines()
    negative = open("negative_words.txt","r").readlines()
    points=0
    for tweets in tmp:
      
      tweets=tweets.split(' ')
      for tword in tweets:
        for pword in positive:
          if tword==pword.rstrip():
            points+=1
            pos+=1
        for nword in negative:
          if tword==nword.rstrip():
            points-=1
            neg+=1
    pos=(float)(pos)
    neg=(float)(neg)
    positive=(float)(pos/(pos+neg))
    print positive
    positive=positive*100
    negative=(float)(neg/(pos+neg))
    print negative
    negative=negative*100
    print ('+ve %',positive)
    print ('-ve %',negative)
    if points>0:
        print "Positive"
    elif points==0:
        print "Neutral"
    else:
        print "Negative"

    sizes = []

    sizes = [pos/float(pos+neg), neg/float(pos+neg)]
    labels = ['Positive','Negative']
    colors = ['yellowgreen','lightcoral']


    plt.pie(sizes,labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
    plt.axis('equal')

    plt.title('sentiment for the celebrity - ' + name2)
    fig_name = "fig_" +name2 + ".png"
    plt.savefig(fig_name)
    plt.show()
    plt.close()
