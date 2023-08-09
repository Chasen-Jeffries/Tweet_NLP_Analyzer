import tweepy

def Get_Tweets():
    # Twitter API credentials
    # Set up authentication with Twitter API
    consumer_key = '6DCuYj5BO1ESHjFY9nvoRtfEL'
    consumer_secret = 'vqrG7WeXwPXJYELvjasgfeSMfTJHI0bzJWKPVy3rugriwXxeUM'
    access_token = '1677130067061907457-MlHy8ZbTYms3BHYrITCVl4ZqV144UA'
    access_token_secret = 'XoNGQmh6IXgguvFFJxzSsf0V09AeWh1zOfq12TM3h8F7W'
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAB2dogEAAAAA391DpZUlmV6CkYM9by56DwANIso%3DwPsZygUn7YPABW6b7XEr0kxqPmziDj8nrFeNcr9NEjBLxTUbhF'

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
