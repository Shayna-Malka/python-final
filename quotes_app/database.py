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

def show_data_in_db():
    with sqlite3.connect("quotes.db") as conn:  # connect to database and automatically close connection
        cur = conn.cursor()  # create cursor
    cur.execute("SELECT quote, author, tags FROM quotes")
    # conn.commit()
    rows= cur.fetchall()
    for row in rows:
        print(row)
    
def add_to_database(tags):
    with sqlite3.connect("quotes.db") as conn:  # connect to database and automatically close connection
        cur = conn.cursor()  # create cursor
      # add quotes to table using web scraping
        quotes =[]
        if len(tags)>1:
            for tag in tags:
                quotes.extend(scrape(f"tag/{tag}/"))
        else:
            quotes.extend(scrape(f"tag/{tag}/"))

        print(len(quotes))
        for quote, author, tags in quotes:
            print("Quote:", quote)
            print("Author:", author)
            print("Tags:", tags)

        conn.executemany("INSERT OR IGNORE INTO quotes VALUES (?, ?, ?)", quotes)
        # conn.commit()
        # extract quotes from database
        cur.execute("SELECT quote, author, tags FROM quotes")
        return cur.fetchall()


# if __name__ == "__main__":
#     main()