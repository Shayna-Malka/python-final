import sqlite3
from web_scraping import scrape
from api import quotes_from_api


# def main():
#     show_data_in_db()


def create_databases():
    with sqlite3.connect("quotes_with_tags.db") as conn:  # connect to database and automatically close connection
        conn.execute("DROP TABLE IF EXISTS quotes_with_tags")
        # conn.execute("DROP TABLE IF EXISTS quotes")
        conn.execute("""  
        CREATE TABLE IF NOT EXISTS quotes_with_tags (
            quote TEXT NOT NULL UNIQUE,
            author TEXT NOT NULL,
            tags TEXT NOT NULL
        )
        """)
    with sqlite3.connect("quotes_without_tags.db") as conn:
        conn.execute("""  
        CREATE TABLE IF NOT EXISTS quotes_without_tags (
            quote TEXT NOT NULL UNIQUE,
            author TEXT NOT NULL
        )
        """)
    # for row in rows: check values were retireved correctly
    #     print(row)

def extract_data_from_tagged_db(tags=[]): #extract_data_from_d
    with sqlite3.connect("quotes_with_tags.db") as conn:  # connect to database and automatically close connection
        cur = conn.cursor()  # create cursor
        if tags==[]:
            cur.execute("SELECT quote, author, tags FROM quotes_with_tags")
        else:
            # placeholders = ",".join(["?"] * len(tags))
            tags_in_query = [f"%{tag}%" for tag in tags]
            # used chatgpt to help build or condition for tags
            cur.execute(f"SELECT * FROM quotes_with_tags WHERE {" OR ".join(["tags LIKE ?"] * len(tags))}", tags_in_query)
    # for row in rows:
    #     print(row)
    return cur.fetchall()

def extract_data_from_untagged_db(limit=50):
    with sqlite3.connect("quotes_without_tags.db") as conn:  # connect to database and automatically close connection
        cur = conn.cursor()  # create cursor
        cur.execute(f"SELECT quote, author FROM quotes_without_tags LIMIT {limit}")

    return cur.fetchall()


def add_data_to_databases(): # added s at end
        quotes_with_tags =[]
        with sqlite3.connect("quotes_with_tags.db") as conn:  # connect to database and automatically close connection
        # cur = conn.cursor()  # create cursor
            # add quotes to table using web scraping
            next_page="/"
            while next_page: #or len(quotes_with_tags) < 50: #there are not so many quotes on site so can extract them all
                data, next_page = scrape(next_page)
                quotes_with_tags.extend(data)
            conn.executemany("INSERT OR IGNORE INTO quotes_with_tags VALUES (?, ?, ?)", quotes_with_tags)

        print("IN ADD DATA: ", len(quotes_with_tags))
        # for quote, author, tags in quotes:
        #     print("Quote:", quote)
        #     print("Author:", author)
        #     print("Tags:", tags)
        quotes_without_tags = []
        with sqlite3.connect("quotes_without_tags.db") as con:  # connect to database and automatically close connection
        # cur = conn.cursor()  # create cursor
            # add quotes to table using api
            data = quotes_from_api()
            quotes_without_tags.extend(data)
            con.executemany("INSERT OR IGNORE INTO quotes_without_tags VALUES (?, ?)", quotes_without_tags)

def add_tags_to_database(tags): # should be update
    with sqlite3.connect("quotes_with_tags.db") as conn:  # connect to database and automatically close connection
        # cur = conn.cursor()  # create cursor
      # add quotes to table using web scraping
        quotes =[]
        if len(tags)>1:
            for tag in tags:
                page = f"tag/{tag}/"
                while page: #and len(quotes) < 5:
                    data, page = scrape(page)
                    quotes.extend(data)
                # quotes.extend(scrape(f"tag/{tag}/"))  # fix will be wrong!! also check in ui
                # check_if_additional_page()
        else:
            page = f"tag/{tag}/"
            while next_page and len(quotes) < 5:
                data, page = scrape(page)
                quotes.extend(data)
            # quotes.extend(scrape(f"tag/{tag}/"))

        # print("IN ADD TAGS", len(quotes))
        # for quote, author, tags in quotes:
        #     print("Quote:", quote)
        #     print("Author:", author)
        #     print("Tags:", tags)

        conn.executemany("INSERT OR IGNORE INTO quotes_with_tags VALUES (?, ?, ?)", quotes)
        # conn.commit()
        # extract quotes from database
        # cur.execute("SELECT quote, author, tags FROM quotes")
        # return cur.fetchall()


# if __name__ == "__main__":
#     main()