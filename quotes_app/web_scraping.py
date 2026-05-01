# importing modules 
import requests 
from bs4 import BeautifulSoup 

def main():
    scrape()

def scrape(parameters =""):   
    try: 
        response = requests.get(f'https://quotes.toscrape.com/{parameters}') # make request
        response.raise_for_status()  # raises exception if request fails

    except requests.RequestException as e: # handle request failure
        return f"Request failed: {e}"
    
    soup = BeautifulSoup(response.text, 'html.parser')  # create soup from content of request
    rows = soup.select(".container .row .col-md-8 .quote") # select applicable classes to extract quotes
    quotes = []
    for row in rows:
        # extract quote details
        quote = row.find("span", class_="text").get_text() 
        if (len(quote)>250): # skip very long quotes 
            continue
        author = row.find("small", class_="author").get_text()
        tags_info = row.find("meta", class_="keywords")
        tags = tags_info["content"].split(",")
        # print(quote, author, tags)
        quotes.append((quote, author, ", ".join(tags))) # store quote info in list
    return quotes

# if __name__ == "__main__":
#     main()