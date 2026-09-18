import os
from dotenv import load_dotenv
import subprocess
import xml.etree.ElementTree as ET
import json
import time
import telegram
from bs4 import BeautifulSoup
import sqlite3
import sqliteFunction


load_dotenv()

newsID = []

chatId = os.getenv("TELEGRAM_CHANNEL_ID")
botToken = os.getenv("TELEGRAM_BOT_TOKEN")

while True:
    result = subprocess.run(
        ["curl", "https://live.financialjuice.com/FJService.asmx/Startup?info=%22EAAAAC6qHO%2FeBUZ05qlPY5XW4m%2BBm9ZyT5mURrFOXEjWWuZGQijiPRltdmem4mruN5mZDZsNXX34purnD0CIkhSyRnxhzSnkqtYMNgtzhwp0tZab0LW9jlLfF5WVyYhP9o9PLAJLDjEKEOY3q9vDqi9n%2Fj8SPi%2F5PadK3CPjMdp72%2BNIzfUiou9Xb%2FmZJc9s5%2BR9ndm%2FCKNsnHE6muHlb6O531LjdL51EkUKS5k5fd3Kfx1qSybhG7dXVPJwR%2BaYIVWeW2ZDAVwZl%2FTY8PdXL0m36OdXjfFyfBBVRkWTQ3zqc8PL%22&TimeOffset=3.5&tabID=0&oldID=0&TickerID=0&FeedCompanyID=0&strSearch=&extraNID=0"],
        capture_output=True,
        text=True
    )
    root = ET.fromstring(result.stdout)
    data = json.loads(root.text)
    data = data["News"]
    for news in data:
        print(news)
        NewsID = news["NewsID"]
        title = news["Title"]
        content = news["Description"]
        published_at = news["DatePublished"]
        Labels = news["Labels"]
        Level = news['Level']
        image_link = news['Img']
        print(f"News ID: {NewsID} | title: {title} | content: {content} | published_at: {published_at}")
        hashtags = []
        if sqliteFunction.check_news_exist(NewsID) == False:
            sqliteFunction.add_news_id(NewsID, title, content, published_at)
            newsID.append(NewsID)
            for label in Labels:
                clean_label = label.replace(' ', '_').replace('-', '_')
                hashtags.append(f"#{clean_label}")

            message = ""
            if 'active-critical' in Level:
                message = "🔴 IMPORTANT: "
            message += f"""
{title}

{BeautifulSoup(content, 'html.parser').get_text()}
"""
            message += " ".join(hashtags)

            print(message.lstrip())

            if news['Img']:
                telegram.send_telegram_photo(chatId, f"https://www.financialjuice.com{image_link}", botToken,
                                             caption=message)
            else:
                telegram.send_telegram_message(chatId, message.lstrip(), botToken)

            print(message)
        else:
            print("not find new news")

    time.sleep(10)

