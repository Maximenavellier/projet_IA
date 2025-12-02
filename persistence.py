import json
import os
from config import RATINGS_FILE

def load_ratings():
    if os.path.exists(RATINGS_FILE):
        try:
            with open(RATINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_ratings(ratings):
    with open(RATINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(ratings, f, indent=4)