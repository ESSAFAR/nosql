# Import MySQL related libraries
import mysql.connector
from mysql.connector import Error
# Import MongoDB client library
from pymongo import MongoClient


class DBHandler:
    """This class contains the attributes and methods to handle database interactions from the scraping program as
    well as the UI tool. """

    def __init__(self):
        """This is the constructor method. It initiates the connection instances with the database."""
        # SQL DB initiation
        try:
            # Create the connection instance as a class level variable by calling "connect" method
            # and supplying the connection details and credentials.
            self.sql_connection = mysql.connector.connect(
                host='localhost',
                port='3306',
                database='pythonapps',
                user='pythonuser',
                password='Welcome1'
            )
            if self.sql_connection.is_connected():
                db_Info = self.sql_connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)

        # Handle exception if connectivity fails
        except Error as e:
            print("Error while connecting to MySQL", e)

        # NoSQL DB initiation
        self.mongo_client = MongoClient(host="localhost", port=27017)
        self.mongo_db = self.mongo_client["local"]
        # Create a class variable for the collection. This will get overwritten with each genre-specific collection
        self.movie_collection = None

    def get_directors(self):
        """This method retrieves the list of Directors from the MySQL DB"""
        # Set the query as a string
        search_query = "SELECT DISTINCT name FROM movieroles WHERE role = 'Director'"
        directors = []
        try:
            # Get the cursor instance
            cursor = self.sql_connection.cursor()
            # Execute the query
            cursor.execute(search_query)
            # get all records
            records = cursor.fetchall()
            print("Total number of rows in table: ", cursor.rowcount)
            # Iterate through the records and append to the list of DTOs
            for row in records:
                # Append the records into the list to return
                directors.append(row[0])
            cursor.close()
        except Error as e:
            # Catch exception and close the cursor
            print("Error while reading data", e)
            if cursor is not None:
                cursor.close()
        return directors

    def get_writers(self):
        """This method retrieves the list of Writers from the MySQL DB"""
        # Set the query as a string
        search_query = "SELECT DISTINCT name FROM movieroles WHERE role = 'Writer'"
        writers = []
        try:
            # Get the cursor instance
            cursor = self.sql_connection.cursor()
            # Execute the query
            cursor.execute(search_query)
            # get all records
            records = cursor.fetchall()
            print("Total number of rows in table: ", cursor.rowcount)
            # Iterate through the records and append to the list of DTOs
            for row in records:
                # Append the records into the list to return
                writers.append(row[0])
            cursor.close()
        except Error as e:
            # Catch exception and close the cursor
            print("Error while reading data", e)
            if cursor is not None:
                cursor.close()
        return writers

    def get_actors(self):
        """This method retrieves the list of Actors from the MySQL DB"""
        # Set the query as a string
        search_query = "SELECT DISTINCT name FROM movieroles WHERE role = 'Star'"
        actors = []
        try:
            # Get the cursor instance
            cursor = self.sql_connection.cursor()
            # Execute the query
            cursor.execute(search_query)
            # get all records
            records = cursor.fetchall()
            print("Total number of rows in table: ", cursor.rowcount)
            # Iterate through the records and append to the list of DTOs
            for row in records:
                # Append the records into the list to return
                actors.append(row[0])
            cursor.close()
        except Error as e:
            # Catch exception and close the cursor
            print("Error while reading data", e)
            if cursor is not None:
                cursor.close()
        return actors

    def get_movies_results(self, genre, director=None, writer=None, actor=None):
        """This method retrieves the records from the genre-specific collection from Mongo db.
           This method accepts values for the director, writer or actor's name to filter within
           list of movies"""
        # Get the collection instance for the genre
        self.movie_collection = self.mongo_db[genre + "boxoffice"]
        # Initiate the list to return
        movies = []
        # Mongo db takes search criteria as dictionary. Initiate the criteria dictionary and the list within it.
        # T
