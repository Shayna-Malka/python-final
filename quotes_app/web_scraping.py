# importing modules 
import requests 
from bs4 import BeautifulSoup 

def main():
    scrape()

def scrape(parameters):   # used to be optioanl ="" 
    try: 
        response = requests.get(f'https://quotes.toscrape.com/{parameters}') # make request
        response.raise_for_status()  # raises exception if request fails

    except requests.RequestException as e: # handle request failure
        # return f"Request failed: {e}"
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')  # create soup from content of request
    rows = soup.select(".container .row .col-md-8 .quote") # select applicable classes to extract quotes
    quotes = []
    for row in rows:
        # extract quote details
        quote = row.find("span", class_="text").get_text() 
        if (len(quote)>100): # skip very long quotes 
            continue
        author = row.find("small", class_="author").get_text()
        tags_info = row.find("meta", class_="keywords")
        tags = tags_info["content"].split(",")
        # print(quote, author, tags)
        quotes.append((quote, author, ", ".join(tags))) # store quote info in list
    another_page = soup.select_one(".next a")
    # soup_for_next_page = None
    next_page_link = ""
    if another_page:
        # soup_for_next_page = soup
        # print(f"ANOTHER PAGE:{another_page["href"]}")
        next_page_link = another_page["href"]
    return quotes, next_page_link

# if __name__ == "__main__":
#     main()