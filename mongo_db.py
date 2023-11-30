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
        'highscore': 0,
        'game_count': 0,
        'completed_game_count': 0
    }
    user_collection.insert_one(user)

def get_user(username):
    user_data = user_collection.find_one({'username': username})
    return user_data

def user_checker(username, password):
    user_creds = user_collection.find_one({'username': username, 'password': password})
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

def leaderboard():
        #https://stackoverflow.com/questions/32076382/mongodb-how-to-get-max-value-from-collections code snipit modified and inserted below
        leaderboardInfo = user_collection.find({},{"_id": 0, "username": 1, "highscore": 1})
        return leaderboardInfo

def check_score(username, new_score, gameCompleted):
    user_collection.update_one({'username': username}, {"$inc": {'game_count': 1}})
    if gameCompleted == "true":
        user_collection.update_one({'username': username}, {"$inc": {'completed_game_count': 1}})
    current_highscore = user_collection.find_one({'username': username})['highscore']
    if new_score > current_highscore:
        user_collection.update_one({'username': username}, {"$set": {'highscore': new_score}})
    else:
        return None