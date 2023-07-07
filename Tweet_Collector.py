import tweepy

def Get_Tweets():
    # Twitter API credentials
    consumer_key = 'YOUR_CONSUMER_KEY'
    consumer_secret = 'YOUR_CONSUMER_SECRET'
    access_token = 'YOUR_ACCESS_TOKEN'
    access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

    # Authenticate with Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # List of Twitter account usernames
    account_list = ['account1', 'account2', 'account3']

    # Dictionary to store tweets for each account
    tweets_dict = {}

    for username in account_list:
        # Collect tweets for the given user
        tweets = tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode='extended').items()

        # Add tweets to the account's list
        tweets_dict[username] = [tweet.full_text for tweet in tweets]
    return tweets_dict

Tweets = Get_Tweets()
