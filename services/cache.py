import json
import os

CACHE_FILE = "cache.json"

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=4)

def add_to_cache(song_id, data):
    cache = load_cache()
    cache[song_id] = data
    save_cache(cache)

def is_cached(song_id):
    cache = load_cache()
    return song_id in cache
