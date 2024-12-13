#main source code

import random
import time
import os
from typing import List
import tweepy
from quotes import listR
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Load environment variables
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")


def get_random_quote() -> str:
    """
    Returns a random quote from the list of quotes.
    """
    return random.choice(listR)


def authenticate_twitter_v2() -> tweepy.Client:
    """
    Authenticates with the Twitter API v2 using environment variables.
    Returns the authenticated Client object.
    """
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
        raise EnvironmentError("Twitter API credentials are not properly set in the .env file.")

    return tweepy.Client(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_SECRET
    )


def tweet_quote_v2(api: tweepy.Client, quote: str) -> None:
    """
    Posts a random quote to Twitter using the Twitter API v2 Client.
    """
    try:
        print("Posting a tweet using v2 API...")
        response = api.create_tweet(text=quote)
        print(f"Tweeted successfully: {response.data['id']}")
    except tweepy.errors.TweepyException as e:
        print(f"An error occurred with Tweepy: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def schedule_tweets(interval_hours: int = 12) -> None:
    """
    Schedules the bot to post a tweet every specified interval of hours.
    """
    api = authenticate_twitter_v2()

    while True:
        tweet_quote_v2(api, get_random_quote())
        print(f"Waiting for the next tweet interval ({interval_hours} hours)...")
        time.sleep(interval_hours * 3600)


if __name__ == "__main__":
    try:
        schedule_tweets(interval_hours=12)
    except KeyboardInterrupt:
        print("Twitter bot stopped manually.")
    except Exception as e:
        print(f"An error occurred: {e}")
