# importing modules 
import requests 
from bs4 import BeautifulSoup 

def main():
    scrape()

def scrape(parameters):
    try: 
        response = requests.get(f'https://quotes.toscrape.com/{parameters}') # make request
        response.raise_for_status()  # raises exception if request fails

    except requests.RequestException as e: # handle request failure
        print(f"Request failed: {e}")
        return [] 
    
    soup = BeautifulSoup(response.text, 'html.parser')  # create soup from content of request
    rows = soup.select(".container .row .col-md-8 .quote") # select applicable classes to extract quotes
    
    quotes = []
    for row in rows:
        # extract quote details
        quote = row.find("span", class_="text").get_text() 
        if (len(quote)>100): # skip long quotes so will be visible is table in streamlit
            continue
        author = row.find("small", class_="author").get_text()
        tags_info = row.find("meta", class_="keywords")
        tags = tags_info["content"].split(",")
        quotes.append((quote, author, ", ".join(tags))) # store quote info in list
    another_page = soup.select_one(".next a") # checks if there's 'next' button on page
    next_page_link = ""
    if another_page:
        next_page_link = another_page["href"]
    return quotes, next_page_link