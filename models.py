from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/fitness_ai')
client = MongoClient(MONGO_URI)
db = client.get_default_database()

users = db.users
plans = db.plans

def create_user(name, email, password_hash):
    doc = {"name": name, "email": email.lower(), "password": password_hash}
    res = users.insert_one(doc)
    return users.find_one({"_id": res.inserted_id})

def get_user_by_email(email):
    return users.find_one({"email": email.lower()})

def get_user_by_id(user_id):
    return users.find_one({"_id": ObjectId(user_id)})

def save_plan(user_id, payload):
    doc = {"user_id": ObjectId(user_id), **payload}
    res = plans.insert_one(doc)
    return plans.find_one({"_id": res.inserted_id})

def get_plan_by_id(plan_id):
    return plans.find_one({"_id": ObjectId(plan_id)})
