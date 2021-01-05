import csv
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

from data.APIkeys import twitter_consumer_key, twitter_consumer_secret, twitter_access_token_key, \
    twitter_access_token_secret
import twitter

twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                          consumer_secret=twitter_consumer_secret,
                          access_token_key=twitter_access_token_key,
                          access_token_secret=twitter_access_token_secret)


# Ophalen gebruikersinfo
def getUser(screen_name):
    user = twitter_api.GetUser(screen_name=screen_name)
    return user


# Aangenomen dat er 3 typen timeline elementen zijn (tweets, retweets en replies)
# Worden hier alleen de tweets opgehaald
def getTweets(user, screen_name):
    timeline = twitter_api.GetUserTimeline(user_id=user.id, screen_name=screen_name, include_rts=False,
                                           trim_user=True, exclude_replies=True)
    return len(timeline)


# Hier worden alle 3 de soorten berichten opgehaald.
# Door er daarna de tweets vanaf te halen hou je de retweets en replies over
def getRetweets(user, screen_name, tweets):
    timeline = twitter_api.GetUserTimeline(user_id=user.id, screen_name=screen_name, include_rts=True,
                                           trim_user=True, exclude_replies=False)
    return len(timeline) - tweets


# Wegschrijven van data evt aanmaken folders/csv bestanden
def writeTwitterInfo(screen_name):
    user = getUser(screen_name=screen_name)
    tweets = getTweets(user=user, screen_name=screen_name)
    retweets = getRetweets(user=user, screen_name=screen_name, tweets=tweets)

    path = 'data/{}'.format(screen_name[1:])

    if not os.path.exists(path):
        os.mkdir(path)

    file = open(path + '/twitterData.csv', 'a', newline='')

    if os.stat('data/{}/twitterData.csv'.format(screen_name[1:])).st_size == 0:
        csv.writer(file, delimiter=';').writerow(['date',
                                                  'user',
                                                  'followers',
                                                  'tweets',
                                                  'retweets'])

    csv.writer(file, delimiter=';').writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                              user.name,
                                              user.followers_count,
                                              tweets,
                                              retweets])
    file.close()


# Verwerken data in grafiek voor opgegeven gebruikersnaam
def createGraph(screen_name):
    f = pd.read_csv('data/{}/twitterData.csv'.format(screen_name[1:]), sep=';')
    f['date'] = pd.to_datetime(f['date'])
    ax = f.plot(kind='line', x='date', y=['tweets', 'retweets'])
    ax2 = f.plot(kind='line', x='date', y='followers', secondary_y=True, ax=ax)
    ax.set_ylabel('Tweets/Retweets')
    ax2.set_ylabel('Followers')
    plt.tight_layout()
    plt.show()
