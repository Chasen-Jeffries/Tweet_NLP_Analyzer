import tweepy
import nltk

from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

from nltk.sentiment import SentimentIntensityAnalyzer

from nltk.corpus import stopwords

import spacy
from spacy.lang.en import English
from spacy import displacy

from collections import Counter

from datetime import datetime, timedelta



# Download required resources
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

# Set up authentication with Twitter API
consumer_key = 'WCe4N89fgFl8uDmBYb4Ganw73'
consumer_secret = 'k9gDvCCBxUOLwQeR7KIh18MiKCFR49MNxpkzKSwL7OTuAKCPrU'
access_token = '1677130067061907457-qmE22Sjtk5DZKXOCwKioT3mP0PNmsX'
access_token_secret = 'X0kXTArSMOr7UXTDd1QHQTQYI6CghvTOeZl9Jd0r5mtLM'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

def Get_Tweets(): 
    # List of Twitter account usernames
    account_list = ['POTUS','JoeBiden']

    # Dictionary to store tweets for each account
    tweets_dict = {}
    
    # Calculate the start and end time for the 24-hour window
    end_time = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=1)

    # Format the time in the required API format
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    for username in account_list:
        # Collect tweets for the given user
        tweets = tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode='extended', since=start_time_str, until=end_time_str).items()

        # Add tweets to the account's list
        tweets_dict[username] = [tweet.full_text for tweet in tweets]
    return tweets_dict

Tweets = Get_Tweets()

# Define the filename for the aggregated file
tweets_dict = Tweets

# Create a new dictionary to store aggregated tweets and statistics
aggregated_tweets_dict = {}

# Construct the NLP pipeline
stop_words = set(stopwords.words('english'))
stop_words.update(['|', '&', '!', '@', '#', '$', '%', '*', '(', ')', '-', '_', "'", ";", ":", ".", ",", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])
porter_stemmer = PorterStemmer()
word_net_lemmatizer = WordNetLemmatizer()

# Load the English language model for SpaCy
nlp = spacy.load('en_core_web_sm')

# Initialize the SentimentIntentsityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Iterate over the tweets_dict and create the aggregated version
for username, tweets in tweets_dict.items():
    # Concatenate all tweets into a document. 
    aggregated_tweets = '\n\n'.join(tweets)
    
    # Calculate statistics for the aggregated tweets
    num_tweets = len(tweets)
    num_chars = sum(len(tweet) for tweet in tweets)
    num_words = sum(len(tweet.split()) for tweet in tweets)
    num_sents = sum(len(tweet.split('.')) for tweet in tweets)
    unique_words = set(word.lower() for tweet in tweets for word in tweet.split())        
    num_vocab = len(unique_words)

    # Clean the text using the NLP pipeline
    cleaned_text = [
        word_net_lemmatizer.lemmatize(porter_stemmer.stem(word.lower()))
        for word in nltk.word_tokenize(aggregated_tweets)
        if word.lower() not in stop_words
    ]

    # Perform Named Entity Recognition (NER)
    doc = nlp(' '.join(cleaned_text))
    ner_tags = [(ent.text, ent.label_) for ent in doc.ents]

    # Count the occurrences of each NER tag
    ner_tag_counts = Counter(ner_tags)

    # Extract the raw count of each mentioned entity
    ner_entities = [ent.text for ent in doc.ents]

    # Count the occurrences of each mentioned entity
    ner_entity_counts = Counter(ner_entities)

    # Perform sentiment analysis for each entity
    entity_sentiment = {}
    for entity, count in ner_entity_counts.items():
        entity_sentiment_scores = []
        for tweet in tweets:
            sentiment_scores = analyzer.polarity_scores(tweet)
            entity_sentiment_scores.append(sentiment_scores['compound'])
        entity_sum_sentiment = sum(entity_sentiment_scores)
        entity_avg_sentiment = entity_sum_sentiment / len(entity_sentiment_scores)
        entity_sentiment[entity] = {
            'Count': count,
            'Sum Sentiment': entity_sum_sentiment,
            'Average Sentiment': entity_avg_sentiment
        }

    # Create a new dictionary entry for the current user
    aggregated_tweets_dict[username] = {
        'Tweets_Doc': cleaned_text,
        'Num_Tweets': num_tweets,
        'Character_Count': num_chars,
        'Word_Count': num_words,
        'Sent_Count': num_sents,
        'Vocab__Count': num_vocab,
        'NER_Tag_Counts': ner_tag_counts,
        'NER_Entity_Counts': ner_entity_counts,
        'NER_Entity_Sentiments': entity_sentiment
    }


# Most least tweets. Who tweets the most and least. 
def Most_Least_Tweets(aggregated_tweets_dict):
    # Sort the users based on the number of tweets in ascending order
    users_sorted_by_tweets = sorted(aggregated_tweets_dict.keys(), key=lambda x: aggregated_tweets_dict[x]['Num_Tweets'])

    # Get the users with the 5 most tweets
    users_with_most_tweets = users_sorted_by_tweets[-10:]

    # Get the users with the 5 fewest tweets
    users_with_fewest_tweets = users_sorted_by_tweets[:10]

    # Print the results
    print("The following individuals have tweeted the most:", ', '.join(users_with_most_tweets))
    print()
    print("The following individuals have tweeted the least:", ', '.join(users_with_fewest_tweets))
    return users_with_most_tweets, users_with_fewest_tweets


# Most CWSV, returns the most and least Characters, Words, Sentences, Vocab
def Most_Least_CWSV(aggregated_tweets_dict):
    ## Characters ##
    # Sort the users based on the number of characters in descending order
    users_sorted_by_chars = sorted(aggregated_tweets_dict.keys(), key=lambda x: aggregated_tweets_dict[x]['Character_Count'])

    # Get the users with the most characters
    users_with_most_chars = users_sorted_by_chars[-5:]

    # Get the users with the least characters
    users_with_fewest_chars = users_sorted_by_chars[:5]
    
    ## Words ##
    # Sort the users based on the number of words in descending order
    users_sorted_by_words = sorted(aggregated_tweets_dict.keys(), key=lambda x: aggregated_tweets_dict[x]['Word_Count'])

    # Get the users with the most words
    users_with_most_words = users_sorted_by_words[-5:]

    # Get the users with the least words
    users_with_fewest_words = users_sorted_by_words[:5]

    ## Sentences ##
    # Sort the users based on the number of sentences in descending order
    users_sorted_by_sents = sorted(aggregated_tweets_dict.keys(), key=lambda x: aggregated_tweets_dict[x]['Sent_Count'])

    # Get the users with the most sentences
    users_with_most_sents = users_sorted_by_sents[-5:]

    # Get the users with the least sentences
    users_with_fewest_sents = users_sorted_by_sents[:5]

    ## Vocab ##
    # Sort the users based on the vocabulary count in descending order
    users_sorted_by_vocab = sorted(aggregated_tweets_dict.keys(), key=lambda x: aggregated_tweets_dict[x]['Vocab_Count'])

    # Get the users with the largest vocabulary
    users_with_most_vocab = users_sorted_by_vocab[-5:]

    # Get the users with the smallest vocabulary
    users_with_fewest_vocab = users_sorted_by_vocab[:5]

    return users_with_most_chars, users_with_fewest_chars, users_with_most_words, users_with_fewest_words, users_with_most_sents, users_with_fewest_sents, users_with_most_vocab, users_with_fewest_vocab

def Most_Least_NER(aggregated_tweets_dict):
    # Extract the NER entity counts from aggregated_tweets_dict
    all_entity_counts = Counter()
    for user_data in aggregated_tweets_dict.values():
        entity_counts = user_data['NER_Entity_Counts']
        all_entity_counts.update(entity_counts)

    # Get the 20 most commonly mentioned entities
    most_common_entities = [entity for entity, count in all_entity_counts.most_common(20)]

    # Initialize dictionaries to store the users with the most and least tweets about each entity
    most_tweets_about_entities = {entity: [] for entity in most_common_entities}
    least_tweets_about_entities = {entity: [] for entity in most_common_entities}
    sentiment_info = {}

    # Iterate over the users' aggregated tweet data
    for username, user_data in aggregated_tweets_dict.items():
        entity_sentiments = user_data['NER_Entity_Sentiments']
        for entity in most_common_entities:
            # Check if the entity is present in the user's tweets
            if entity in entity_sentiments:
                sentiment = entity_sentiments[entity]['Average Sentiment']
                count = entity_sentiments[entity]['Count']
                # Append the username and sentiment to the appropriate list based on tweet count
                if count == max(entity_sentiments.values(), key=lambda x: x['Count'])['Count']:
                    most_tweets_about_entities[entity].append(username)
                elif count == min(entity_sentiments.values(), key=lambda x: x['Count'])['Count']:
                    least_tweets_about_entities[entity].append(username)
                # Save sentiment information
                if username not in sentiment_info:
                    sentiment_info[username] = {}
                sentiment_info[username][entity] = sentiment

    return most_tweets_about_entities, least_tweets_about_entities, sentiment_info, 



##########
# Tweets:

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



# Call the Most_Least_NER function to get the users with the most and least tweets about each entity
most_tweets_about_entities, least_tweets_about_entities, sentiment_info = Most_Least_NER(aggregated_tweets_dict)

# Call the Most_Least_NER function to get the most and least mentioned entities
most_tweets_about_entities, least_tweets_about_entities, sentiment_info = Most_Least_NER(aggregated_tweets_dict)

# Call the tweet_most_least_tweeters function
tweet_most_least_tweeters(api, aggregated_tweets_dict)

# Call the tweet_most_least_CWSV function
tweet_most_least_CWSV(api, aggregated_tweets_dict)

# Call the tweet_information function
tweet_NER_sentiment_20_MC_Entity(api, most_tweets_about_entities, sentiment_info)

# Call the tweet the most mentioned entitites
tweet_most_mentioned_entities(api, most_tweets_about_entities)

