import sys
import requests
import json


def main():
    try:
        # api_request_random_quote()
        quotes_from_api()
    except TypeError:  # handle invalid input
        sys.exit(1)
# Inspiration, Motivation Friendship, Courage, Truth
def api_request_random_quote():
    try:
        response = requests.get("https://dummyjson.com/quotes/random")
        response.raise_for_status()
    except requests.HTTPError:
        raise

    content = response.json()  # convert response into json format
    # print("\nFull response: ")
    # print(json.dumps(content, indent=4))  # displays full json response in easier format to read
    return content

def quotes_from_api():
    try:
        response = requests.get("https://dummyjson.com/quotes?limit=300")
        response.raise_for_status()
    except requests.HTTPError:
        raise
    quotes = []
    content = response.json()  # convert response into json format
    print("Full response: ", len(content["quotes"]))
    for q_info in content["quotes"]:
        quote = q_info["quote"]
        author = q_info["author"]
        quotes.append((quote, author))
    # print(json.dumps(content, indent=4))  # displays full json response in easier format to read
    # for q in quotes:
    #     print(q)
    return quotes

if __name__ == "__main__":
    main()