import sqlite3
from web_scraping import scrape


# def main():
#     show_data_in_db()


def create_database():
    with sqlite3.connect("quotes.db") as conn:  # connect to database and automatically close connection
        conn.execute("DROP TABLE IF EXISTS quotes")
        conn.execute("""  
        CREATE TABLE IF NOT EXISTS quotes (
            quote TEXT NOT NULL UNIQUE,
            author TEXT NOT NULL,
            tags TEXT NOT NULL
        )
        """)
    # for row in rows: check values were retireved correctly
    #     print(row)

def extract_data_from_db(tags=[]):
    with sqlite3.connect("quotes.db") as conn:  # connect to database and automatically close connection
        cur = conn.cursor()  # create cursor
        if tags==[]:
            cur.execute("SELECT quote, author, tags FROM quotes")
        else:
            # placeholders = ",".join(["?"] * len(tags))
            tags_in_query = [f"%{tag}%" for tag in tags]
            # used chatgpt to help build or condition for tags
            cur.execute(f"SELECT * FROM quotes") # WHERE {" OR ".join(["tags LIKE ?"] * len(tags))}", tags_in_query)
    # for row in rows:
    #     print(row)
    return cur.fetchall()

def add_data_to_database():
        quotes =[]
        with sqlite3.connect("quotes.db") as conn:  # connect to database and automatically close connection
        # cur = conn.cursor()  # create cursor
            # add quotes to table using web scraping
            next_page=""
            while next_page or len(quotes) < 200:
                data, next_page = scrape(next_page)
                quotes.extend(data)
            conn.executemany("INSERT OR IGNORE INTO quotes VALUES (?, ?, ?)", quotes)

        print("IN ADD DATA: ", len(quotes))
        # for quote, author, tags in quotes:
        #     print("Quote:", quote)
        #     print("Author:", author)
        #     print("Tags:", tags)


def add_tags_to_database(tags): # should be update
    with sqlite3.connect("quotes.db") as conn:  # connect to database and automatically close connection
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

        conn.executemany("INSERT OR IGNORE INTO quotes VALUES (?, ?, ?)", quotes)
        # conn.commit()
        # extract quotes from database
        # cur.execute("SELECT quote, author, tags FROM quotes")
        # return cur.fetchall()


# if __name__ == "__main__":
#     main()