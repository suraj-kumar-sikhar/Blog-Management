from pymongo import MongoClient
from datetime import datetime
import random

client = MongoClient("mongodb+srv://surajsikhar:ZexjUF3guemq2asQ@inovaare.4c0gsrl.mongodb.net/")
db = client["blog"]         # 🔁 Replace with your DB name
collection = db["blogs"]            # 🔁 Replace if your collection name differs

categories = [
    "activism",
    "memoirs",
    "lifestyles",
    "technology",
    "education",
    "science",
    "travel"
]

authors = [
    "Aarav Roy", "Maya Das", "Kabir Khan", "Nina Bose", 
    "Ishaan Dev", "Tara Mehta", "Rahul Sen"
]

titles = [
    "Deep Dive into", "Reflections on", "Exploring", "The Beauty of",
    "Challenges in", "Empowering Stories from", "Future of"
]

image_base_url = "https://source.unsplash.com/600x400/?"

sample_blogs = []

# Generate 10 blogs per category
for category in categories:
    for i in range(20):
        blog = {
            "title": f"{random.choice(titles)} {category.title()} #{i+1}",
            "author": random.choice(authors),
            "email": f"{category}{i}@example.com",
            "category": category,
            "content": f"This is a blog about {category}. " + ("x" * 150),
            "approved": True,
            "image": f"{image_base_url}{category}",
            "published": datetime.utcnow()
        }
        sample_blogs.append(blog)

# Optional: Clear existing approved blogs
collection.delete_many({"approved": True})

# Insert into DB
collection.insert_many(sample_blogs)
print(f"✅ Inserted {len(sample_blogs)} blog posts across 7 categories.")
