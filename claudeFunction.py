import json

def create_news_clustering_prompt(news_list):
    prompt = """
You are a professional news clustering AI.
Your task is to group news articles that describe the same real-world event.
Clustering rules:

    Treat a single speech, press conference, interview, testimony, public appearance, earnings call, meeting, or official briefing as ONE event.
    If multiple news articles contain different quotes, statements, or headlines from the same speech, press conference, interview, meeting, or briefing, they MUST be grouped together, even if each article focuses on a different topic or quote.
    For example, if Donald Trump gives one speech and one article is about tariffs, another about China, and another about interest rates, all of them belong to the same group because they originated from the same speech.
    Likewise, statements released during the same FOMC meeting, ECB press conference, White House briefing, earnings call, or government press conference should be treated as one event.
    Articles about the same speech, announcement, military action, attack, accident, meeting, decision, interview, phone call, visit, court ruling, signing ceremony, earnings report, economic data release, or incident must be grouped together.
    Follow-up reports, reactions, confirmations, official statements, damage assessments, and additional details about the same incident belong to the same group.
    Group articles only when they refer to the exact same real-world event.
    Do NOT group articles simply because they mention the same country, person, organization, company, or topic.
    Different speeches by the same person are different events.
    Different meetings involving the same participants are different events.
    Different military operations, attacks, or announcements must remain separate even if they involve the same countries or organizations.
    Each news article can belong to only one group.
    If an article has no related articles, create a group containing only that article.
    Same-country macro data grouping: Economic data releases from the same country (e.g., retail sales, unemployment rate, inflation, GDP) published by the same national statistics institute or central bank should be grouped together as a single event, even if they cover different indicators. Each country has its own separate group.

Ignore rules:

    Ignore any item that is NOT a real news event.
    Do NOT include market preparation posts, session preparation posts, recurring scheduled reports, calendars, watchlists, promotional posts, navigation items, or general informational content.
    These items must be completely excluded from the output JSON.
    Examples of content that must be ignored:
    "US session prep"
    "Europe session prep"
    "Asia session prep"
    "Morning juice"
    "FinancialJuice"
    "financial juice"
    "Currency strength chart report"
    "Currency strength report"
    "Market overview"
    "Daily market update"
    "Trading session outlook"
    "Economic calendar overview"
    "Market sentiment report"
    Do not create groups for ignored items.
    Do not include ignored items as single-item groups.
    Only include articles that describe an actual real-world event, announcement, statement, decision, speech, meeting, military action, accident, earnings release, economic data release, legal action, or other genuine news event.

Output rules:

    Return ONLY valid JSON.
    Do NOT use Markdown.
    Do NOT include ```json.
    Do NOT add explanations or comments.
    Always use exactly this JSON structure:

{
  "groups": [
    {
      "event": "Short description of the real-world event",
      "news_ids": [1, 2, 3]
    }
  ]
}

Use the "id" field from each article for the news_ids array.

News articles:
"""

    news_json = []

    for row in news_list:
        news_json.append({
            "id": row[0],
            "newsID": row[1],
            "title": row[2],
            "content": row[3],
            "published_at": row[4]
        })

    prompt += json.dumps(news_json, ensure_ascii=False, indent=2)

    return prompt
