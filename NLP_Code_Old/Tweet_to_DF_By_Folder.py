# Folder Loop for Uncompressed JSON files
import os
import pandas as pd
import json
import nltk

from nltk.corpus import stopwords

from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

import spacy
from spacy.lang.en import English
from spacy import displacy

from collections import Counter

from nltk.sentiment import SentimentIntensityAnalyzer

# Specify the path to the folder containing the JSON files
folder_path = 'Tweets_Corpus/06-2017'

# List all JSON files in the folder
json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

# Initialize lists to store all the data
data = []

 # Construct the NLP pipeline
stop_words = set(stopwords.words('english'))
stop_words.update(['|', '&', '!', '@', '#', '$', '%', '*', '(', ')', '-', '_', "'", ";", ":", ".", ",", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])
porter_stemmer = PorterStemmer()
word_net_lemmatizer = WordNetLemmatizer()

# Load the English language model for SpaCy
nlp = spacy.load('en_core_web_sm')

# Initialize the SentimentIntentsityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Process each JSON file
for json_file in json_files:
    file_path = os.path.join(folder_path, json_file)

    # Read the JSON file and load the data
    with open(file_path, 'r', encoding='utf-8') as file:
        tweets_data = json.load(file)

    for tweet in tweets_data:     
        # Extract relevant information for each tweet
        username = tweet['screen_name']
        # Convert the 'time_of_tweet' to datetime format
        time_of_tweet = pd.to_datetime(tweet['time'])
        # Extract the date and time of day separately
        date = time_of_tweet.date()
        time_of_day = time_of_tweet.time()
        full_tweet_text = tweet['text']

        # Calculate statistics for the aggregated tweets
        num_tweets = len(tweets_data)
        num_chars = len(full_tweet_text)
        num_words = len(full_tweet_text.split())
        num_sents = len(full_tweet_text.split('.'))
        unique_words = set(word.lower() for word in full_tweet_text.split())
        num_vocab = len(unique_words)

        # Clean the text using the NLP pipeline
        cleaned_text = [
            word_net_lemmatizer.lemmatize(porter_stemmer.stem(word.lower()))
            for word in nltk.word_tokenize(full_tweet_text)
            if word.lower() not in stop_words
        ]
        # Append the data to the list (each tweet's data is appended separately)
        data.append([username, date, time_of_day, full_tweet_text, cleaned_text, num_tweets, num_chars, num_words, num_sents, num_vocab])

# Create a DataFrame from the collected data
columns = ['username', 'date', 'time', 'full_tweet_text', 'cleaned_text', 'num_tweets', 'num_chars', 'num_words', 'num_sents', 'num_vocab']
US_Legislative_Tweets = pd.DataFrame(data, columns=columns)

# Create a dictionary to store entity names and their sentiment scores
entity_sentiments_dict = {}

# Process each tweet's cleaned text for NER and sentiment analysis
for cleaned_text in US_Legislative_Tweets['cleaned_text']:
    # Perform Named Entity Recognition (NER)
    doc = nlp(' '.join(cleaned_text))
    ner_entities = [ent.text for ent in doc.ents]

    # Calculate entity sentiment for the current tweet
    for entity in ner_entities:
        sentiment_scores = analyzer.polarity_scores(entity)
        entity_sentiments_dict[entity] = entity_sentiments_dict.get(entity, []) + [sentiment_scores['compound']]

# Find the maximum number of entity sentiment scores for padding
max_entities = max(len(scores) for scores in entity_sentiments_dict.values()) if entity_sentiments_dict else 0

# Pad the entity sentiment scores with zeros to ensure the same number of values for each entity
for entity, scores in entity_sentiments_dict.items():
    entity_sentiments_dict[entity].extend([0] * (max_entities - len(scores)))

# Create a DataFrame for entity sentiment scores
entity_sentiments_df = pd.DataFrame(entity_sentiments_dict)

# Concatenate the entity sentiment DataFrame with the main DataFrame
US_Legislative_Tweets = pd.concat([US_Legislative_Tweets, entity_sentiments_df], axis=1)

# Export the result DataFrame to a CSV file
US_Legislative_Tweets.to_csv('US_Legislative_Tweets.csv', index=False)
