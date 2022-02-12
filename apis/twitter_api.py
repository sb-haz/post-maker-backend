"""
Imports
"""
import tweepy
import re
import html

import credentials.twitter_credentials


"""
Twitter API Client
"""
def getClient():
    try:
        client = tweepy.Client(bearer_token=credentials.bearer_token,
                               consumer_key=credentials.consumer_key,
                               consumer_secret=credentials.consumer_secret,
                               access_token=None, access_token_secret=None)
        return client
    except Exception as e:
        print(e)


"""
Get info from tweet
"""
def getTweetInfo(tweet_id):

    # Get api client
    client = getClient()

    # Call endpoint
    try:
        tweet = client.get_tweet(tweet_id,
                                 expansions="author_id,attachments.media_keys")
    except Exception as e:
        print(e)

    # Get tweet status text and remove links and convert chars
    # e.g. &amp -> &
    tweet_text = tweet.data['text']
    tweet_text = re.sub(r"http\S+", "", tweet_text)
    tweet_text = html.unescape(tweet_text)

    # Get tweet author
    tweet_author = tweet.includes["users"][0]["username"]

    # Media type, if any
    media_keys = []
    try:
        media_type = tweet.includes["media"][0]["type"]
        media_keys = tweet.data["attachments"]["media_keys"]
    except:
        media_type = "none"

    # Return tweet data
    return tweet_text, tweet_author, media_type
