import csv
import json
from pymongo import MongoClient

def insert_csv_to_mongodb(csv_file, mongo_config, db_name, collection_name):
    """
    Inserts data from a CSV file into a MongoDB collection.

    :param csv_file: Path to the CSV file to be inserted.
    :param mongo_config: Dictionary containing MongoDB connection parameters.
                          Example: {
                              "host": "your_host",
                              "port": your_port,
                              "username": "your_username",
                              "password": "your_password",
                              "authSource": "admin"
                          }
    :param db_name: The name of the MongoDB database.
    :param collection_name: The name of the MongoDB collection.
    """
    # Create MongoDB client
    client = MongoClient(mongo_config['host'], mongo_config['port'], 
                         username=mongo_config.get('username'), 
                         password=mongo_config.get('password'), 
                         authSource=mongo_config.get('authSource'))
    
    # Connect to the database and collection
    db = client[db_name]
    collection = db[collection_name]

    # Open the CSV file and read data
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        # Prepare the data to insert (convert each row to a dictionary)
        documents = []
        for row in csv_reader:
            documents.append(dict(row))

    # Insert data into MongoDB collection
    try:
        # Insert documents into the collection
        result = collection.insert_many(documents)
        print(f"Successfully inserted {len(result.inserted_ids)} records into the '{collection_name}' collection.")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Close the MongoDB connection
        client.close()

def insert_json_to_mongodb(json_file, mongo_config, db_name, collection_name):
    """Writes data from a JSON file into a MongoDB collection (list of JSONs)"""
    try:
        # Create MongoDB client
        client = MongoClient(mongo_config['host'], mongo_config['port'], 
                            username=mongo_config.get('username'), 
                            password=mongo_config.get('password'), 
                            authSource=mongo_config.get('authSource'))
        
        # Connect to the database and collection
        db = client[db_name]
        collection = db[collection_name]
        
        with open(json_file, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):
                collection.insert_many(data)
            else:
                collection.insert_one(data)
        
        print(f"Data from '{json_file}' written to collection '{collection_name}' in database '{db_name}'")
    except Exception as e:
        print(f"An error occurred while writing to the collection: {e}")


# csv data
csv_file = 'cycling-network-4326.csv'
mongo_config = {
    "host": "localhost",
    "port": 27017,
    "username": "mongoadmin",
    "password": "mongoadmin",
    "authSource": "admin"
}
db_name = 'fireball'
collection_name = 'cycling-network'

insert_csv_to_mongodb(csv_file, mongo_config, db_name, collection_name)

# json data
json_file = 'station_data.json'
collection_name = 'station-data'
insert_json_to_mongodb(json_file, mongo_config, db_name, collection_name)
