import os
import json
import random
import requests
from datetime import datetime

# ========== সিক্রেটস লোড ==========
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

# ========== কোন কোন কী মিসিং, তা পরীক্ষা করা ==========
missing_keys = []
if not BOT_TOKEN:
    missing_keys.append("BOT_TOKEN")
if not CHANNEL_ID:
    missing_keys.append("CHANNEL_ID")
if not NEWS_API_KEY:
    missing_keys.append("NEWS_API_KEY")

if missing_keys:
    print(f"❌ ERROR: These secrets are MISSING in GitHub Actions: {', '.join(missing_keys)}")
    print("🔧 Please add them in: Repo -> Settings -> Secrets and variables -> Actions")
    exit(1)
else:
    print("✅ All secrets found successfully!")

POSTED_FILE = 'posted_news.json'

def load_posted():
    try:
        with open(POSTED_FILE, 'r') as f:
            return set(json.load(f))
    except:
        return set()

def save_posted(posted_set):
    with open(POSTED_FILE, 'w') as f:
        json.dump(list(posted_set), f)

# ========== নিউজ ফেচ ==========
def fetch_tech_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "(web development OR AI OR programming OR JavaScript OR Python OR applications) AND -cricket -football -politics",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=20)
        data = resp.json()
        if data.get('status') == 'ok':
            return data.get('articles', [])
        else:
            print(f"API Error: {data.get('message')}")
            return []
    except Exception as e:
        print(f"Fetch Error: {e}")
        return []

# ========== ফরম্যাটিং ==========
def format_news_post(articles):
    posted = load_posted()
    new_articles = []
    
    for art in articles:
        title = art.get('title', '')
        if title in posted or '[Removed]' in title or not title:
            continue
        new_articles.append(art)
    
    if not new_articles:
        return None

    selected = random.sample(new_articles, min(3, len(new_articles)))
    
    html_parts = []
    html_parts.append("<b>📰 TODAY'S TECH DIGEST</b>")
    html_parts.append("──────────────────")
    
    for idx, art in enumerate(selected, 1):
        title = art.get('title', '').replace('<', '&lt;').replace('>', '&gt;')
        desc = art.get('description', '')
        if desc:
            desc = desc.replace('<', '&lt;').replace('>', '&gt;')
            if len(desc) > 90:
                desc = desc[:90] + '...'
        
        html_parts.append(f"<b>▫️ {idx}. {title}</b>")
        if desc:
            html_parts.append(f"   {desc}")
        html_parts.append("")
    
    html_parts.append("──────────────────")
    html_parts.append("💡 <b>Want a Stunning Website?</b> Contact @hacker_52")
    
    for art in selected:
        posted.add(art.get('title'))
    save_posted(posted)
    
    return "\n".join(html_parts)

def send_post(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    return requests.post(url, json=payload)

def main():
    print("🚀 Fetching latest news...")
    articles = fetch_tech_news()
    
    if not articles:
        print("⚠️ No articles. Sending fallback.")
        send_post("<b>📡 No new tech news right now.</b>\nCheck back later!")
        return
    
    post_text = format_news_post(articles)
    if not post_text:
        print("📭 No new unique news. Skipping.")
        return
    
    result = send_post(post_text)
    if result.status_code == 200:
        print("✅ Posted successfully!")
    else:
        print(f"❌ Failed: {result.text}")

if __name__ == "__main__":
    main()
