# intal code given from mongodb https://www.mongodb.com/docs/drivers/pymongo/
# mongodb tutorial https://www.geeksforgeeks.org/mongodb-python-insert-update-data/#
from pymongo import MongoClient
uri = "mongodb+srv://admin:BrownieBuddy007@cluster0.azusdwd.mongodb.net/"
# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# database
db = client.pt_game

# collections
user_collection = db.users
element_collection = db.elements

# ACCOUNT FUNCTIONS
def account_create(username, password, email):
    # user account structure in user_collection
    user = {
        'username': username,
        'password': password,
        'email': email,
        'highscore': 0
    }
    user_collection.insert_one(user)

def login_checker(username, password):
    # how to use find_one https://www.geeksforgeeks.org/python-mongodb-find_one-query/#
    user_creds = user_collection.find_one({'username': username, 'password': password})
    # user_id = user_creds["_id"]
    if user_creds:
        return True
    else:
        return False

def username_checker(username):
    # check for taken username
    username_finder = user_collection.find_one({'username': username})
    if username_finder:
        return True
    else:
        return False
