# This file creates connections with databases
from neo4j import GraphDatabase
# Import necessary libraries
from pymongo import MongoClient
# from neo4j import GraphDatabase

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "book_management"
MONGO_COLLECTION = "books"

# Neo4j Configuration
NEO4J_URI = "bolt://localhost"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4jneo4j"

# MongoDB client setup
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB]
mongo_collection = mongo_db[MONGO_COLLECTION]

# Neo4j driver setup
neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
