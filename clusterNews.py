import os
from dotenv import load_dotenv
from anthropic import Anthropic
import sqliteFunction
import claudeFunction
import json
import re
import telegram
import time

load_dotenv()

chatId = os.getenv("TELEGRAM_CHANNEL_ID")
botToken = os.getenv("TELEGRAM_BOT_TOKEN")
claude_api_key = os.getenv("CLAUDE_API_TOKEN")


# گرفتن اخبار
newsList = sqliteFunction.get_news(8)

# ساخت prompt
prompt = claudeFunction.create_news_clustering_prompt(newsList)

client = Anthropic(
    api_key=claude_api_key
)

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=8192,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
print(response)
claude_result = next(
    block.text
    for block in response.content
    if block.type == "text"
)
print(claude_result)

# حذف ```json و ```
claude_result = re.sub(r"```json\s*", "", claude_result)
claude_result = re.sub(r"```", "", claude_result)

# حذف فاصله‌های اضافی
claude_result = claude_result.strip()

# تبدیل JSON به dict
clusters = json.loads(claude_result)

grouped_news = []

for group in clusters["groups"]:

    event = group["event"]
    news_ids = group["news_ids"]

    news_items = []

    for news_id in news_ids:
        news = sqliteFunction.get_news_by_id(news_id)

        if news:
            news_items.append(news)


    # چسباندن متن خبرهای یک event
    combined_text = "\n\n".join(
        [
            f"{item[2]}\n{item[3]}"
            for item in news_items
        ]
    )


    grouped_news.append({
        "event": event,
        "news_count": len(news_items),
        "text": combined_text
    })

for item in grouped_news:

    message = (
        f"<b>{item['event']}</b>\n\n"
        f"{item['text']}"
    )
    time.sleep(1)    
    telegram.send_telegram_message(chatId,message.lstrip(),botToken)
    #send_telegram(message)
print(json.dumps(grouped_news, indent=2, ensure_ascii=False))
