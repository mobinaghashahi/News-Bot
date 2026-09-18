import sqlite3
from time import sleep

conn = sqlite3.connect("news.db")
cursor=conn.cursor()

def add_news_id(id, title=None, content=None, published_at=None):
    if content == "":
        content = "empty"
        print(f"Content is empty.")


    cursor.execute(
    "INSERT INTO news (newsID, title, content, published_at) VALUES (?, ?, ?, ?)",
    (id, title, content, published_at)
)
    conn.commit()
def check_news_exist(id):
    data=cursor.execute(f"SELECT * FROM news where newsID ={id}")
    data=data.fetchall()
    if data:
        return True
    else:
        #add_news_id(id)
        return False
    #for dataT in data:
    #    print(dataT[1])

def get_news(hours):
    query = """
    SELECT *
    FROM news
    WHERE datetime(published_at) >= datetime('now', '+3 hours', '+30 minutes', ?)
    ORDER BY datetime(published_at) ASC
    """

    data = cursor.execute(query, (f'-{hours} hours',))
    return data.fetchall()


def get_news_by_id(newsID):
    query = """
    SELECT *
    FROM news
    WHERE id = ?
    """

    data = cursor.execute(query, (newsID,))
    return data.fetchone()
