import tweepy

# Set up authentication with Twitter API
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)


# Function to tweet the list of users who tweeted the most and the fewest
def tweet_most_least_tweeters(api, aggregated_tweets_dict):
    # Call the Most_Least_Tweets function to get the users with the most and fewest tweets
    users_with_most_tweets, users_with_fewest_tweets = Most_Least_Tweets(aggregated_tweets_dict)

    # Compose the tweet for the most tweeters
    most_tweeters_tweet = "The ten individuals who tweeted the most:\n"
    most_tweeters_tweet += ", ".join(users_with_most_tweets)

    # Compose the tweet for the least tweeters
    least_tweeters_tweet = "Top ten individuals who tweeted the fewest:\n"
    least_tweeters_tweet += ", ".join(users_with_fewest_tweets)

    # Send the tweets
    api.update_status(most_tweeters_tweet)
    api.update_status(least_tweeters_tweet)


# Function to tweet the list of users who tweeted the most and the fewest
import tweepy

# Function to tweet the most and least CWSV (Characters, Words, Sentences, Vocabulary)
def tweet_most_least_CWSV(api, aggregated_tweets_dict):
    # Call the Most_Least_CWSV function to get the users with the most and least CWSV
    users_with_most_chars, users_with_fewest_chars, users_with_most_words, users_with_fewest_words, users_with_most_sents, users_with_fewest_sents, users_with_most_vocab, users_with_fewest_vocab = Most_Least_CWSV(aggregated_tweets_dict)

    # Compose the tweets
    tweets = [
        f"The following individuals have used the most characters: {', '.join(users_with_most_chars)}",
        f"The following individuals have used the least characters: {', '.join(users_with_fewest_chars)}",
        f"The following individuals have used the most words: {', '.join(users_with_most_words)}",
        f"The following individuals have used the least words: {', '.join(users_with_fewest_words)}",
        f"The following individuals have used the most sentences: {', '.join(users_with_most_sents)}",
        f"The following individuals have used the least sentences: {', '.join(users_with_fewest_sents)}",
        f"The following individuals have used the largest vocabulary: {', '.join(users_with_most_vocab)}",
        f"The following individuals have used the smallest vocabulary: {', '.join(users_with_fewest_vocab)}"
    ]

    # Send the tweets
    for tweet in tweets:
        api.update_status(tweet)


# Function to tweet the 20 most mentioned entities
def tweet_most_mentioned_entities(api, most_mentioned_entities):
    # Compose the tweet message
    tweet = "The 20 Most Mentioned Entities Today:n"
    entity_strings = [f"{entity}: {count}" for entity, count in most_mentioned_entities]
    tweet += ", ".join(entity_strings)

    # Send the tweet
    api.update_status(tweet)


# Tweet NER Sentiment analysis on the 20 most common entities 
def tweet_NER_sentiment_20_MC_Entity(api, most_tweets_about_entities, sentiment_info):
    # Iterate over the most common (MC) entities
    for entity, users in most_tweets_about_entities.items():
        # Create separate tweets for each entity
        positive_users = []
        negative_users = []

        # Categorize users based on sentiment
        for user in users:
            sentiment = sentiment_info[user][entity]
            if sentiment > 0:
                positive_users.append(user)
            elif sentiment < 0:
                negative_users.append(user)

        # Add positive users to the tweet
        if positive_users:
            tweet += f"The following individuals had a positive sentiment towards {entity}:\n"
            tweet += ", ".join(positive_users)

        # Add negative users to the tweet
        if negative_users:
            tweet += f"The following individuals had a negative sentiment towards {entity}:\n"
            tweet += ", ".join(negative_users)
            tweet += "\n"

        # Send the tweet
        api.update_status(tweet)



# Call the tweet_most_least_tweeters function
tweet_most_least_tweeters(api, aggregated_tweets_dict)

# Call the tweet_most_least_CWSV function
tweet_most_least_CWSV(api, aggregated_tweets_dict)

# Call the tweet_information function
tweet_NER_sentiment_20_MC_Entity(api, most_tweets_about_entities, sentiment_info)

# Call the tweet the most mentioned entitites
tweet_most_mentioned_entities(api, most_mentioned_entities)

