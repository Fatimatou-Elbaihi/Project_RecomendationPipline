from neo4j import GraphDatabase
from pymongo import MongoClient
from datetime import datetime
import secrets  # Importing secrets module for generating passwords

# Neo4j connection details
neo_uri = "bolt://localhost:7687"
neo_username = "neo4j"
neo_password = "passeword"

# MongoDB connection details
mongo_uri = "mongodb+srv://usename:password@cluster0.bvpyv8d.mongodb.net/"
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client["database"]
mongo_collection = mongo_db["collection"]

# Connect to Neo4j
print("Connecting to Neo4j...")
neo_driver = GraphDatabase.driver(neo_uri, auth=(neo_username, neo_password))
print("Connected to Neo4j.")

## Define function to execute Neo4j query and insert into MongoDB
def insert_user_profiles_and_tweets():
    with neo_driver.session() as neo_session:
        # Cypher query to retrieve user data with their tweets from Neo4j
        print("Executing Cypher query in Neo4j...")
        neo_query = """
        MATCH (u:User)-[:POSTS]->(t:Tweet)
        RETURN u.id AS id, u.name AS name, u.screen_name AS username, 
               u.email AS email, u.profile_image_url AS profile_picture_url,
               u.location AS location, u.bio AS bio,
               collect(t.id) AS tweet_ids
        LIMIT 4;
        """
        result = neo_session.run(neo_query)
        print("Cypher query executed.")

        # Iterate over result and insert into MongoDB
        print("Inserting user profiles and tweets into MongoDB...")
        for record in result:
            # Generate a random password for each user
            generated_password = secrets.token_urlsafe(12)
            # Insert user profile along with their tweets
            user_dict = {
                "id": record["id"],
                "username": record["username"],
                "password": generated_password,
                "email": record["email"],  # Add email address
                "profile_picture_url": record["profile_picture_url"],  # Add profile picture URL
                "location": record["location"],  # Add location
                "bio": record["bio"],  # Add bio description
                "tweets": record["tweet_ids"]  # Store tweet IDs as an array
            }
            mongo_collection.insert_one(user_dict)
        print("User profiles and tweets inserted into MongoDB.")

# Execute the function
print("Executing data insertion process...")
insert_user_profiles_and_tweets()
print("Data insertion process completed.")
