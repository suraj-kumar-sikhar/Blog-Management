from pymongo import MongoClient

client = MongoClient("mongodb+srv://surajsikhar:ZexjUF3guemq2asQ@inovaare.4c0gsrl.mongodb.net/")
db = client["blog"]
blogs_collection = db["blogs"]
