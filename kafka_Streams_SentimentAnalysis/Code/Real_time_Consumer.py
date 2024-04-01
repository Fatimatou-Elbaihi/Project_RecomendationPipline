import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from textblob import TextBlob

# Kafka connection details
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092,localhost:9093,localhost:9094'  # Update with Kafka broker addresses
KAFKA_TWITTER_TOPIC = 'twitter_data'
KAFKA_SENTIMENT_TOPIC = 'sentiment'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to Kafka consumer
consumer = KafkaConsumer(KAFKA_TWITTER_TOPIC,
                         bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Connect to Kafka producer
producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Function to perform sentiment analysis
def analyze_sentiment(tweet_text):
    if tweet_text is None:
        return 'unknown'  # Or any other default value or handling you prefer
    analysis = TextBlob(tweet_text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# Consumer loop
for message in consumer:
    tweet_data = message.value
    tweet_text = tweet_data['tweet_text']
    tweet_id = tweet_data['tweet_id']  # Retrieve tweet ID from the message
    
    # Perform sentiment analysis
    sentiment = analyze_sentiment(tweet_text)
    
    # Add sentiment and tweet ID to the tweet data
    tweet_data['sentiment'] = sentiment
    tweet_data['tweet_id'] = tweet_id
    
    # Publish the analyzed data to the 'sentiment' topic
    producer.send(KAFKA_SENTIMENT_TOPIC, value=tweet_data)
    
    # Log the processing
    logging.info("Processed tweet from 'twitter_data' topic with sentiment analysis. Tweet ID: %s, Sentiment: %s", tweet_id, sentiment)
