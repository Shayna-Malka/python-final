import sys
import requests
import json
import random

def api_request_random_quote():
    try:
        response = requests.get("https://dummyjson.com/quotes/random")
        response.raise_for_status()
    except requests.HTTPError:
        print("API Error requesting random quote")
        return extract_data_from_untagged_db(random.randint(0, 30))[random.randint(0, 10)]

    content = response.json()
    return content

def quotes_from_api():
    try:
        response = requests.get("https://dummyjson.com/quotes?limit=300")
        response.raise_for_status()
    except requests.HTTPError:
        print("API Error requesting quotes")
        return 
    quotes = []
    content = response.json()
    print("Full response: ", len(content["quotes"]))
    for q_info in content["quotes"]:
        quote = q_info["quote"]
        author = q_info["author"]
        quotes.append((quote, author))
    return quotes
