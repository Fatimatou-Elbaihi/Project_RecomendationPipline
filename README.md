# Project Overview:

The goal of this project is to develop a graph-based recommendation system for Twitter or similar social media platforms. This recommendation system suggests hashtags to browse and/or users to follow based on users' activities and sentiments. The project involves a front-end web application for posting tweets, which are then processed and used to update an underlying graph database. Sentiment analysis is performed on the tweets in near real-time, and the results are used to further refine recommendations. The primary focus is on building a scalable pipeline rather than the sophistication of the web application or the recommendations themselves.

## Project Components:

 ### Kafka Setup:
 Apache Kafka is used to facilitate communication between producers and consumers. Three Kafka servers (brokers) are configured for fault tolerance and scalability. Configuration files for each server (server1.properties, server2.properties, and server3.properties) are created with unique IDs (id=0, id=1 , id=3) and port numbers.
Start zookeeper, the following comands should runned inside C:/kafka for easly using the comands:

#### Batch Processing: A batch producer (BatchProducer.py) is used to produce data from Neo4j to the Kafka topic named twitter_data. The FromBeginningConsumer.py consumes all data from the twitter_data topic and sends it to the sentiment topic.
### Real-Time Processing: The Stream_Producer.py fetches data to the twitter_data topic based on the timestamp to ensure that only newly inserted tweets are streamed and consumed by the Real_time_consumer.py, which is suitable for recommendation purposes.
in each consumer there is a function analyze_sentiment that uses textblob library to perform sentiment analysis of the twitter and classify twitter to ( 'unknown' if it is none, 'positive', 'negative' or 'neutral') and and sentiment to record of twit to be send to topic 'sentiment'.
Configuration Steps:

#### Modify Server Properties: Copy the server.properties file three times as server1.properties, server2.properties, and server3.properties. Adjust the content of each file by assigning different IDs and port numbers.
Set Log Directory Paths: Update the log.dirs variable in server.properties to store logs permanently in a specified directory (e.g., c:/kafka/kafka-logs). Similarly, update the dataDir variable in zookeeper.properties to set the path for Zookeeper logs.
Note: It's recommended to create folders within the log directory for each server to better manage and identify logs.
example server2:
```
id= 1
```
```
log.dirs=c:/kafka/kafka-logs/server2
```
```
listeners=PLAINTEXT://:9093
```
inside zookeeper.proprieties set the path of log files:
```
dataDir=c:/kafka/zookeeper-logs
```
### Start kafka:
You will need to open five terminals, one in which you start zookeeper, three for starting the brokers and one for writting comands to check the servers connections, create topics or list topics created:
Start zookeeper, the following comands should runned inside C:/kafka: 
```
C:/kafka/bin/windows/zookeeper-server-start.bat C:/kafka/kafka_2.13-3.5.0/config/zookeeper.properties 
```
Start first kafka-server:
``` 
C:/kafka/bin/windows/kafka-server-start.bat C:/kafka/config/server1.properties 
```
```
C:/kafka/bin/windows/kafka-server-start.bat C:/kafka/config/server2.properties 
```
```
C:/kafka/bin/windows/kafka-server-start.bat C:/kafka/config/server3.properties 
```
Create topic1: 
```
C:/kafka/bin/windows/kafka-topics.bat --create --twitter_data --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --replication-factor 1 --partitions 5
```
Create topic2: 
```
C:/kafka/bin/windows/kafka-topics.bat --create --twitter_data --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --replication-factor 1 --partitions 5
```
comand list topics to check if topic have been created :
```
C:/kafka/bin/windows/kafka-topics.bat --list --bootstrap-server localhost:9092,localhost:9093,localhost:9094
```
Comand to check server connection in windows prompt:
```
jps
```
Make sure in case of want it to cancel all the serversers and restart the project to delete all the log files in (kafka-logs/server1, kafka-logs/server2, kafka-logs/server3) and also the logs of zookeeper based on your specified path
 bacause this may cause problems.
## /MongoDB_Schema/


This folder contains a Python script named neo4jToMongoDb.py. This script loads information for three users and generates unique codes for security puposes for each user. These codes are intended for later use in a web interface to insert real-time new tweets. Additionally, the file database.collection.json simply contains the exported results from MongoDB.

## /Neo4j-Connect/Configuration/
Aiming to make neo4j to acces to our data
change the following line to enable kafka connector to be able to access to distributed 'sentiment' to make change on 
nodes in neo4j by adding the sentiment propriety. The following are configurations to be done in order to build neo4j-connector locally:
first we add kafka-neo4j-connector jar file to be downloaded for [Link Text](https://www.confluent.io/hub/neo4j/kafka-connect-neo4j) make sure to be compatibale with your kafka version and added to where kafka jar files resides 'C:\kafka\libs' and add the path to connect-distributed.properties file in the following line:
```
plugin.path=C:/kafka/libs
```
add also the three diferent ports:
```
# A list of host/port pairs to use for establishing the initial connection to the Kafka cluster.
bootstrap.servers=localhost:9092,localhost:9093,localhost:9094
```
 The we need to start kafka connector in the folder wher we inatalled kakfka C:\kafka\config run the following comand in terminal:
```
.\bin\windows\connect-distributed.bat config\connect-distributed.properties
```
neo4j sink file need to be configured based on your topic name and neo4j loging info
neo4j querry in sink.json file, you may want to check [Link Text](https://neo4j.com/docs/kafka/kafka-connect/) for further details:
```
MERGE (n:Tweet {id: event.tweet_id}) SET n.sentiment = event.sentiment
```
Then we need to run the following comand in terminal(windows):
```
Invoke-RestMethod -Method Post -Uri "http://localhost:8083/connectors" `
  -ContentType "application/json" `
  -InFile "path\\to\\sink.json"
```

