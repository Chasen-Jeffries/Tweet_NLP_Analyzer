# US Congress Tweets NLP Analysis 
This project focuses on analyzing politicians' tweets using natural language processing (NLP) techniques. The goal is to identify political consistency and sentiments on various topics based on the content of their tweets. The project involves aggregating tweets from different politicians, performing NLP tasks such as sentiment analysis and named entity recognition (NER), and generating insights from the gathered data.

## Features
The project includes the following features:

- Data Collection: Tweets from various politicians are collected and stored in a dictionary format using the tweets_dict data structure.
- NLP Pipeline: The collected tweets are processed using an NLP pipeline, which includes tasks such as text cleaning, stemming, lemmatization, stop-word removal, and named entity recognition.
- Sentiment Analysis: The SentimentIntensityAnalyzer from the NLTK library is utilized to perform sentiment analysis on the tweets. It calculates sentiment scores for each tweet and aggregates sentiment information for identified entities.
- Named Entity Recognition (NER): The SpaCy library is used for named entity recognition. It identifies named entities in the cleaned text and categorizes them into predefined entity types such as persons, organizations, locations, etc.
- Aggregation and Statistics: The project aggregates the tweets from each politician, calculates various statistics such as the number of tweets, characters, words, sentences, vocabulary size, and tracks the count of different named entities.
- Identification of Most/Least Active Tweeters: The project identifies the politicians who have tweeted the most and the least, based on the number of tweets. It provides insights into the activity levels of different politicians.
- Identification of Most/Least CWSV: The project determines the politicians with the highest and lowest counts for characters, words, sentences, and vocabulary. This analysis provides insights into the linguistic aspects of their tweets.
- Sentiment Analysis on Most Common Entities: The project identifies the 20 most commonly mentioned entities in the tweets and determines the sentiment of politicians towards those entities. It highlights which politicians have positive or negative sentiments towards specific entities.

## Usage
To use this project, follow these steps:
1. Set up the required dependencies by running pip install -r requirements.txt.
2. Load in the dataset from [alexlitel-congresstweets](https://github.com/alexlitel/congresstweets)
3. Run the main script to start the analysis. This script will collect tweets, perform NLP tasks, calculate statistics, and generate insights.
4. The generated insights and analysis results can be viewed through the console output. The most active tweeters, CWSV information, and sentiment towards common entities will be displayed.

## Future Enhancements
This project lays the foundation for further enhancements. Some potential areas of improvement and expansion include:

- Fine-tuning Sentiment Analysis Models: Fine-tune sentiment analysis models to better capture nuanced sentiments and improve accuracy. This could involve training models on domain-specific data related to politics and politicians' tweets.
- Topic Modeling: Incorporate topic modeling techniques to identify the most prevalent topics in politicians' tweets.This could provide insights into the key issues and discussions surrounding political figures.
- Network Analysis: Implement network analysis to explore relationships and interactions between politicians based on their mentions and retweets. Analyzing the network structure could reveal influential figures, alliances, and patterns of information flow.
- Consistency Scores: Develop consistency scores to measure how consistently positive or negative politicians' sentiments are towards specific entities. This analysis can provide insights into their ideological alignment and consistency in expressing sentiments.
- Accountability Score: Introduce an accountability score to evaluate how closely politicians' tweets align with their campaign promises. A gold standard list of campaign promises, based on their official campaign websites or public statements, can be used as a reference for comparison.
- Gold Standard for NER: Create a curated list of entities specifically tailored for politicians and their tweets. This gold standard list can enhance the accuracy and relevance of the named entity recognition (NER) process, providing more meaningful insights into the entities mentioned by politicians.
- Web-based Dashboard or Visualization: Develop a web-based dashboard or visualization tool to present the analysis results in an interactive and user-friendly manner. This can include visualizations of sentiment trends, network graphs, topic clusters, and other relevant visual representations of the data.
- Expanded Dataset: Expand the dataset to include more politicians and gather tweets over an extended period to capture temporal patterns and trends. This can enhance the comprehensiveness and diversity of the analysis, providing a broader understanding of politicians' sentiments and behaviors.

## Contributions
Contributions to this project are welcome. If you have any suggestions, improvements, or new features, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Dataset
https://github.com/alexlitel/congresstweets

## Acknowledgments
- This project utilizes the NLTK and SpaCy libraries for natural language processing tasks.
