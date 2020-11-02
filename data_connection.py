from pymongo import MongoClient


def connect_to_db():
    # Connect to MongoDB - Note: Change connection string as needed
    connection_client = MongoClient(port=27017)
    db = connection_client.alarinka
    print("Connected to database")
    return db


def check_record_exist(record_name):
    db = connect_to_db()
    record = db.vehicles.find_one({'record_id': record_name})
    print("Checked record in database", record)
    if record:
        return True
    return False


def save_new_record(record_data):
    if record_data:
        db = connect_to_db()
        result = db.vehicles.insert_one(record_data)
        print("Record saved successfully: {0}".format(result.inserted_id))
        return result.inserted_id
    return None
