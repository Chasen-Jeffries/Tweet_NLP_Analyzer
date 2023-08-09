import tweepy
import pandas as pd
 
# Fill the X's with the credentials obtained by
# following the above mentioned procedure.
consumer_key = '6DCuYj5BO1ESHjFY9nvoRtfEL'
consumer_secret = 'vqrG7WeXwPXJYELvjasgfeSMfTJHI0bzJWKPVy3rugriwXxeUM'
access_token = '1677130067061907457-MlHy8ZbTYms3BHYrITCVl4ZqV144UA'
access_token_secret = 'XoNGQmh6IXgguvFFJxzSsf0V09AeWh1zOfq12TM3h8F7W'
 
#Pass in our twitter API authentication key
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)

#Instantiate the tweepy API
api = tweepy.API(auth, wait_on_rate_limit=True)


search_query = "'ref''world cup'-filter:retweets AND -filter:replies AND -filter:links"
no_of_tweets = 100

try:
    #The number of tweets we want to retrieved from the search
    tweets = api.search_tweets(q=search_query, lang="en", count=no_of_tweets, tweet_mode ='extended')
    
    #Pulling Some attributes from the tweet
    attributes_container = [[tweet.user.name, tweet.created_at, tweet.favorite_count, tweet.source, tweet.full_text] for tweet in tweets]

    #Creation of column list to rename the columns in the dataframe
    columns = ["User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"]
    
    #Creation of Dataframe
    tweets_df = pd.DataFrame(attributes_container, columns=columns)
except BaseException as e:
    print('Status Failed On,',str(e))
 

