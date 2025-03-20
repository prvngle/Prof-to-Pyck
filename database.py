import json
import os

database = "prof_reviews.json"

def reviews():
    if not os.path.exists(database):
        save_reviews([])
        return []
    
    with open(database) as db:
        try:
            return json.load(db)
        except json.JSONDecodeError:
            return []
        
def save_reviews(reviews):
    with open(database, "w") as db:
        json.dump(reviews, db, indent=2)
