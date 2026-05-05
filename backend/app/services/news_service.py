import feedparser
from app.core.config import RSS_URL, NEWS_LIMIT

def fetch_news() -> list[str]:
    feed = feedparser.parse(RSS_URL)
    articles = []
    for entry in feed.entries[:NEWS_LIMIT]:
        articles.append(entry.title)
    return articles
