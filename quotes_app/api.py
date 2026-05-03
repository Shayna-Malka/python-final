import sys
import requests
import json


def main():
    try:
        api_request_random_quote()
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

if __name__ == "__main__":
    main()