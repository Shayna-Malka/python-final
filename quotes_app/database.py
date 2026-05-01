import sqlite3

def create_database():
    with sqlite3.connect("quotes.db") as conn:  # connect to database and automatically close connection
        cur = conn.cursor()  # create cursor

        # create quotes table
        cur.execute("DROP TABLE IF EXISTS quotes")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            quote TEXT NOT NULL,
            author TEXT NOT NULL,
            tags TEXT NOT NULL
        )
        """)
        # add guests to table :)
        quotes = [
            ("You are amazing", "Chaya", "Inspiration"),
            ("Smile - it's free!", "Batya", "Inspiration"),
            ("Emes", "Moshe", "Truth"),
            ("The tough get going when the going gets tough", "Rabbi M", "Inspirational"),
        ]
        cur.executemany("INSERT INTO quotes VALUES (?, ?, ?)", quotes)
        conn.commit()
        # extract guests from database
        cur.execute("SELECT quote, author, tags FROM quotes")
        return cur.fetchall()

    # for row in rows: check values were retireved correctly
    #     print(row)
