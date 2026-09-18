# 📈 Financial News Telegram Bot

A Python-based Telegram bot that monitors **FinancialJuice** for newly published financial news and delivers them to a Telegram channel in near real-time.

The bot is designed for **low-latency news delivery**, with a typical delay of **less than 5 seconds** between detecting a new article and publishing it to Telegram.

In addition to real-time news delivery, the project includes an AI-powered news clustering system using **Claude** to analyze and categorize news from the previous 8 hours.

---

## ✨ Features

### ⚡ Real-Time News Monitoring

The bot continuously monitors:

> https://www.financialjuice.com/

When a new news item is detected, it is processed and published to the configured Telegram channel.

The system is optimized for low latency and normally publishes new items with a delay of **under 5 seconds**.

---

### 🏷️ Automatic News Tags

News items are published together with relevant tags.

Example:

```text
🇺🇸 FED
💵 USD
📈 STOCKS
🏦 CENTRAL BANK
```

Tags make it easier to quickly identify the market or topic related to each news item.

---

### 🔴 Important News Detection

Important market-moving news can be highlighted using:

```text
🔴 IMPORTANT
```

Example:

```text
🔴 IMPORTANT

FED: Interest rates will remain unchanged.

#FED #USD #FOMC
```

This allows users to quickly distinguish potentially significant announcements from regular news flow.

---

## 🤖 AI News Clustering

The project also includes a separate script:

```text
clusterNews.py
```

This script analyzes news from the **previous 8 hours** and sends them to **Claude** using a predefined prompt.

Claude analyzes the collected news and groups related stories into categories/clusters.

For example, several separate headlines related to the Federal Reserve can be grouped together:

```text
Federal Reserve
├── Interest rate expectations
├── Powell comments
├── Inflation data
└── Treasury market reaction
```

This makes it easier to understand the major themes and events that occurred during the previous trading session.

---

## 🏗️ Architecture

The project consists of two main components.

```text
                    ┌──────────────────────┐
                    │   FinancialJuice     │
                    │      Website         │
                    └──────────┬───────────┘
                               │
                               │ Real-time monitoring
                               ▼
                    ┌──────────────────────┐
                    │    Python Bot        │
                    │                      │
                    │  • Fetch News         │
                    │  • Detect New Items   │
                    │  • Process Tags       │
                    │  • Detect Important   │
                    └──────────┬───────────┘
                               │
                         Save / Check
                               │
                               ▼
                    ┌──────────────────────┐
                    │       SQLite         │
                    │      Database        │
                    └──────────────────────┘
                               │
                               │ Publish
                               ▼
                    ┌──────────────────────┐
                    │   Telegram Channel   │
                    └──────────────────────┘


                    ┌──────────────────────┐
                    │    SQLite / News     │
                    │    Previous 8 Hours  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   clusterNews.py     │
                    └──────────┬───────────┘
                               │
                               │ Prompt
                               ▼
                    ┌──────────────────────┐
                    │       Claude         │
                    │    AI Clustering     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Categorized /        │
                    │ Clustered News       │
                    └──────────────────────┘
```

---

## 🗄️ Database

The project uses **SQLite** as its database engine.

SQLite was selected because the application primarily needs lightweight local persistence rather than a large database server.

The database is used to keep track of processed news and prevent duplicate publications.

A typical workflow is:

```text
New News
   │
   ▼
Check SQLite
   │
   ├── Already exists ──► Ignore
   │
   └── New
        │
        ▼
     Save News
        │
        ▼
 Publish to Telegram
```

This allows the bot to restart without repeatedly publishing the same news.

---

## 📁 Project Structure

A simplified project structure looks like this:

```text
financial-news-bot/
│
├── main.py
├── clusterNews.py
├── sqliteFunction.py
├── .env
├── requirements.txt
├── README.md
│
└── database/
    └── news.db
```

> The exact filenames can be changed depending on the final project structure.

### `main.py`

The main real-time news monitoring process.

Responsibilities include:

* Connecting to FinancialJuice
* Detecting new news
* Processing news information
* Handling tags
* Detecting important news
* Saving news into SQLite
* Publishing news to Telegram

### `clusterNews.py`

The AI analysis component.

Responsibilities include:

* Reading news from the previous 8 hours
* Preparing the Claude prompt
* Sending news to Claude
* Receiving the AI response
* Clustering related news
* Categorizing major events

### `sqliteFunction.py`

Contains database-related functions such as:

* Creating database tables
* Inserting news
* Checking for duplicate news
* Retrieving historical news
* Retrieving the last 8 hours of news

---

## 🔐 Environment Variables

Sensitive configuration should not be stored directly inside the source code.

Create a `.env` file:

```env
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
TELEGRAM_CHANNEL_ID=YOUR_TELEGRAM_CHANNEL_ID
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY
```

Then load the variables in Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
api_key = os.getenv("ANTHROPIC_API_KEY")
```

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
*.db
__pycache__/
```

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/financial-news-bot.git
cd financial-news-bot
```

Create a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the `.env` file and then start the bot:

```bash
python main.py
```

---

## 🤖 Running the AI Clustering

The clustering process is independent from the real-time news collector.

Run:

```bash
python clusterNews.py
```

The script retrieves news from the previous **8 hours**, sends the relevant data to Claude, and processes the returned clusters.

It can also be scheduled using a system scheduler such as:

### Linux Cron

```cron
0 * * * * /path/to/venv/bin/python /path/to/project/clusterNews.py
```

This example runs the clustering process every hour.

---

## 🔄 Data Flow

### Real-Time Pipeline

```text
FinancialJuice
      │
      ▼
Fetch New News
      │
      ▼
Extract News Data
      │
      ▼
Check SQLite
      │
      ├── Duplicate ──► Skip
      │
      ▼
Store News
      │
      ▼
Process Tags
      │
      ▼
Important News?
      │
   ┌──┴──┐
   │     │
  YES    NO
   │     │
   ▼     ▼
🔴 IMPORTANT
   │
   └───────► Telegram
```

### AI Clustering Pipeline

```text
SQLite
  │
  │ Last 8 Hours
  ▼
clusterNews.py
  │
  ▼
Build Prompt
  │
  ▼
Claude API
  │
  ▼
Analyze News
  │
  ▼
Group Related News
  │
  ▼
Categorized Results
```

---

## ⏱️ Performance

The primary real-time component is designed around low-latency news delivery.

Target:

```text
News published on FinancialJuice
              ↓
       Detection by Bot
              ↓
       Processing
              ↓
      Telegram Publish
              ↓
         < 5 seconds
```

Actual latency can vary depending on:

* FinancialJuice response time
* Network latency
* Telegram API response time
* Server performance
* Temporary connectivity issues

---

## 🧠 Why SQLite?

SQLite provides several advantages for this project:

* Zero database server configuration
* Very low resource usage
* Simple deployment
* Easy backup
* Suitable for a single bot process
* Fast enough for the project's workload

The database primarily acts as a lightweight persistence and deduplication layer.

---

## 🔒 Security

Do **not** commit credentials or API keys to Git.

Never upload:

```text
.env
Telegram Bot Token
Telegram Channel credentials
Anthropic API Key
Database files containing sensitive information
```

Use environment variables instead.

---

## ⚠️ Disclaimer

This project is intended for **technical and informational purposes**.

The news collected from FinancialJuice and the AI-generated classifications are provided as information and should not be considered financial advice.

AI-generated clustering may contain errors or misclassification. Always verify important information against the original source.

---

## 🛠️ Technologies

The project is built using:

* 🐍 **Python**
* 📡 **FinancialJuice**
* 📱 **Telegram Bot API**
* 🗄️ **SQLite**
* 🤖 **Anthropic Claude**
* 🔐 **python-dotenv**

---

## 🚀 Future Improvements

Possible future improvements include:

* [ ] Multi-channel support
* [ ] More advanced news categorization
* [ ] Priority levels beyond `IMPORTANT`
* [ ] Historical news dashboard
* [ ] Web-based monitoring panel
* [ ] Redis-based high-performance caching
* [ ] PostgreSQL support
* [ ] Automatic health monitoring
* [ ] Telegram inline commands
* [ ] News search
* [ ] Performance and latency monitoring
* [ ] Automatic retry mechanism
* [ ] Docker deployment
* [ ] Structured logging
---

## 👨‍💻 Author

Developed as a Python-based financial news monitoring and AI news-analysis system.

**Real-time financial news → Telegram → AI-powered clustering**
