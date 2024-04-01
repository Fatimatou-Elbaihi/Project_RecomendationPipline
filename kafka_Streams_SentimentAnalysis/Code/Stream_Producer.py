import time
import json
import logging
from neo4j import GraphDatabase
from kafka import KafkaProducer

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "passeword"

# Kafka connection details
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092,localhost:9093,localhost:9094'  # Update with Kafka broker addresses
KAFKA_TOPIC = 'twitter_data'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Connect to Kafka producer
producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Function to fetch data from Neo4j and publish to Kafka
def fetch_and_publish_data():
    with driver.session() as session:
        try:
            #Query that orders twits by timestamptime
            result = session.run("MATCH (u:User)-[:POSTS]->(t:Tweet)RETURN u.name AS name, u.screen_name AS username, t.text AS tweet_text ORDER BY t.timestamp ASC LIMIT 100")

            for record in result:
                tweet_data = {
                    'name': record['name'],
                    'username': record['username'],
                    'tweet_text': record['tweet_text']
                }
                producer.send(KAFKA_TOPIC, value=tweet_data)
                logging.info("Published tweet to Kafka: %s", tweet_data)
        except Exception as e:
            logging.error("Error fetching or publishing data: %s", e)

# Main function to run the producer
def main():
    try:
        while True:
            fetch_and_publish_data()
            time.sleep(60)  # Fetch data every 60 seconds
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt detected. Closing connections...")
    finally:
        driver.close()
        producer.close()

if __name__ == "__main__":
    main()
