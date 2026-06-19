import os
import json
import random
import requests
import urllib.parse
from datetime import datetime

# ==================================================
# ১. সিক্রেটস লোড
# ==================================================
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
UNSPLASH_API_KEY = os.environ.get('UNSPLASH_API_KEY')

if not all([BOT_TOKEN, CHANNEL_ID, NEWS_API_KEY, GEMINI_API_KEY]):
    print("❌ ERROR: BOT_TOKEN, CHANNEL_ID, NEWS_API_KEY, GEMINI_API_KEY missing!")
    exit(1)

POSTED_FILE = 'posted_topics.json'

def load_posted():
    try:
        with open(POSTED_FILE, 'r') as f:
            return set(json.load(f))
    except:
        return set()

def save_posted(posted_set):
    with open(POSTED_FILE, 'w') as f:
        json.dump(list(posted_set), f)

# ==================================================
# ২. নিউজ ফেচ (শুধু ওয়েব/অ্যাপ/কোডিং)
# ==================================================
def fetch_trending_topic():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": '("web development" OR "app development" OR software OR programming OR React OR Python OR JavaScript OR Flutter OR API OR "frontend" OR "backend" OR "full stack") -cricket -football -politics -AI -Claude -Gemini',
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 8,
        "apiKey": NEWS_API_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=20)
        data = resp.json()
        if data.get('status') == 'ok':
            articles = data.get('articles', [])
            for art in articles:
                title = art.get('title', '')
                if '[Removed]' in title or not title:
                    continue
                clean_title = title.split('-')[0].strip()
                clean_title = clean_title.split('|')[0].strip()
                return clean_title
        else:
            print(f"API Error: {data.get('message')}")
    except Exception as e:
        print(f"Fetch Error: {e}")
    
    return "Latest Web Development Frameworks in 2026"

# ==================================================
# ৩. জেমিনি দিয়ে প্রো লেভেল কন্টেন্ট লেখা (ইমোজি বাদ)
# ==================================================
def generate_ai_content(topic):
    prompt = f"""Write a short, professional, and insightful tech news update (70-90 words) about this development topic: "{topic}".
    Write in a clear, journalistic style with 2 short paragraphs. Do not use emojis or hashtags.
    Keep the tone polished and informative, like a Wired or TechCrunch article.
    Output only plain text with normal punctuation and line breaks."""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"⚠️ Gemini Error: {e}")
        return f"Developers are exploring new possibilities in {topic}. This shift is shaping modern software architecture and improving developer productivity across the board."

# ==================================================
# ৪. ইমেজ ফেচ (Unsplash + ব্যাকআপ)
# ==================================================
def fetch_image_guaranteed(query):
    if UNSPLASH_API_KEY:
        url = f"https://api.unsplash.com/photos/random?query={query}&orientation=landscape&count=1"
        headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    print("✅ Image from Unsplash")
                    return data[0]['urls']['regular']
        except Exception as e:
            print(f"⚠️ Unsplash Error: {e}")
    
    print("🔄 Generating AI image...")
    image_prompt = f"modern web development coding technology, clean design"
    encoded_prompt = urllib.parse.quote(image_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=600&nologo=true"

# ==================================================
# ৫. ফাইনাল ফরম্যাটিং (Haku DEV Brand - মিনিমালিস্ট)
# ==================================================
def format_premium_post(topic, ai_text):
    """
    সম্পূর্ণ ক্লিন, প্রোফেশনাল, বক্স/ডট মুক্ত
    """
    lines = []
    # হেডার
    lines.append("")
    lines.append("✦  HAKU DEV  ✦")
    lines.append("")
    lines.append("————————————————————————————")
    lines.append("")
    # টপিক (বোল্ড)
    lines.append(f"{topic}")
    lines.append("")
    # কন্টেন্ট (AI থেকে আসা)
    lines.append(ai_text)
    lines.append("")
    # ফুটার ডিভাইডার
    lines.append("————————————————————————————")
    lines.append("")
    # ফুটার টেক্সট
    lines.append("Contact  @hacker_52  |  Web & App Development")
    
    return "\n".join(lines)

# ==================================================
# ৬. ইনলাইন বাটন
# ==================================================
def create_inline_button():
    return {
        "inline_keyboard": [
            [{"text": "📩 Connect with Haku", "url": "https://t.me/hacker_52"}]
        ]
    }

# ==================================================
# ৭. টেলিগ্রামে পোস্ট সেন্ড
# ==================================================
def send_photo_post(image_url, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHANNEL_ID,
        "photo": image_url,
        "caption": caption,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "reply_markup": create_inline_button()
    }
    return requests.post(url, json=payload)

# ==================================================
# ৮. মেইন
# ==================================================
def main():
    print("🚀 Haku DEV Bot is starting...")
    
    raw_topic = fetch_trending_topic()
    topic = raw_topic[:80]
    
    posted = load_posted()
    if topic in posted:
        print(f"📭 Already posted: {topic}. Skipping.")
        return
    
    print(f"📌 Topic: {topic}")
    
    ai_text = generate_ai_content(topic)
    caption = format_premium_post(topic, ai_text)
    image_url = fetch_image_guaranteed("web development")
    
    result = send_photo_post(image_url, caption)
    
    if result.status_code == 200:
        posted.add(topic)
        save_posted(posted)
        print("✅ Posted successfully with Premium Haku DEV style!")
    else:
        print(f"❌ Failed: {result.text}")

if __name__ == "__main__":
    main()
