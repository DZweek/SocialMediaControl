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


def getuser(screen_name):
    user = twitter_api.GetUser(screen_name=screen_name)
    return user


def gettweets(user, screen_name):
    timeline = twitter_api.GetUserTimeline(user_id=user.id, screen_name=screen_name, include_rts=False,
                                           exclude_replies=False)
    return len(timeline)


def getretweets(user, screen_name, tweets):
    timeline = twitter_api.GetUserTimeline(user_id=user.id, screen_name=screen_name, include_rts=True,
                                           exclude_replies=True)
    return len(timeline) - tweets


def writetwitterinfo(screen_name):
    user = getuser(screen_name=screen_name)
    tweets = gettweets(user=user, screen_name=screen_name)
    retweets = getretweets(user=user, screen_name=screen_name, tweets=tweets)

    f = open('data/twitterData.csv', 'a', newline='')

    if os.stat('data/twitterData.csv').st_size == 0:
        csv.writer(f, delimiter=';').writerow(['date',
                                               'user',
                                               'followers',
                                               'tweets',
                                               'retweets'])

    csv.writer(f, delimiter=';').writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                           user.name,
                                           user.followers_count,
                                           tweets,
                                           retweets])
    f.close()


def createGraph():
    f = pd.read_csv('data/twitterData.csv', sep=';')
    ax = f.plot(kind='line', x='date', y=['tweets', 'retweets'])
    ax2 = f.plot(kind='line', x='date', y='followers', secondary_y=True, ax=ax)
    ax.set_ylabel('Tweets/Retweets')
    ax2.set_ylabel('Followers')
    plt.tight_layout()
    plt.show()
