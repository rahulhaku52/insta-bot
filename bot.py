import os
import random
import requests
import urllib.parse
from datetime import datetime

# ==================================================
# ১. গিটহাব সিক্রেটস থেকে সব API কী লোড করা
# ==================================================
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
UNSPLASH_API_KEY = os.environ.get('UNSPLASH_API_KEY')

# যদি কোনো কী মিসিং থাকে, তাহলে এরর দেখাবে
if not all([BOT_TOKEN, CHANNEL_ID, GEMINI_API_KEY, UNSPLASH_API_KEY]):
    print("❌ ERROR: Secrets missing! Set BOT_TOKEN, CHANNEL_ID, GEMINI_API_KEY, UNSPLASH_API_KEY")
    exit(1)

# ==================================================
# ২. টপিকের তালিকা (শুধু টেক, এআই, গেম, ওয়েব ডেভ)
# ==================================================
TOPICS = [
    "Latest AI Tools 2026",
    "New Game Releases",
    "Python vs Rust Coding",
    "Web Development Trends",
    "Cyber Security Tips",
    "Future of JavaScript",
    "AI in Game Development",
    "Startup Tech Ideas",
    "Cloud Computing Innovations",
    "Best Programming IDEs"
]

# ==================================================
# ৩. কন্টেন্ট জেনারেট (Google Gemini AI)
# ==================================================
def generate_ai_content(topic):
    """Gemini API দিয়ে ১০০% নতুন ইংলিশ পোস্ট তৈরি করে"""
    prompt = f"""Write a short, exciting, and highly engaging social media post (max 120 words) about "{topic}". 
    Make it sound like breaking tech news. Use emojis, proper line breaks, and an enthusiastic tone. 
    Output only plain text with emojis, no markdown."""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        text = data['candidates'][0]['content']['parts'][0]['text']
        return text
    except Exception as e:
        print(f"⚠️ AI Error: {e}")
        # AI কাজ না করলে একটি ডিফল্ট ফ্রেশ টেক্সট
        return f"🔥 Big updates are coming in the world of {topic}! Stay ahead of the curve with the latest tech innovations. 🚀"

# ==================================================
# ৪. ছবি আনা (Unsplash + Pollinations ব্যাকআপ)
# ==================================================
def fetch_image_guaranteed(query):
    """ছবি বাধ্যতামূলকভাবে আনে (Unsplash ফেল করলে AI জেনারেট করে)"""
    
    # ১. প্রথমে Unsplash চেষ্টা
    url = f"https://api.unsplash.com/photos/random?query={query}&orientation=landscape&count=1"
    headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print("✅ Image fetched from Unsplash")
                return data[0]['urls']['regular']
    except Exception as e:
        print(f"⚠️ Unsplash Error: {e}")
    
    # ২. Unsplash কাজ না করলে Pollinations.ai (ফ্রি, কোনো API কী লাগে না)
    print("🔄 Generating AI image via Pollinations.ai...")
    image_prompt = f"futuristic {query} technology concept, clean design, 4k"
    encoded_prompt = urllib.parse.quote(image_prompt)
    fallback_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=600&nologo=true"
    return fallback_url

# ==================================================
# ৫. ফ্যাশনেবল ফুটার (প্রমোশন)
# ==================================================
def create_footer():
    return (
        "\n\n━━━━━━━━━━━━━━━━━━━━━━\n"
        "✨ *Want a Stunning Website?* ✨\n"
        "🔥 Professional Design | Fast Delivery\n"
        "📩 **Contact me now:** @hacker_52\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )

# ==================================================
# ৬. টেলিগ্রামে পোস্ট পাঠানো
# ==================================================
def send_post_to_channel(image_url, caption):
    """Telegram এ Photo হিসেবে পোস্ট পাঠায়"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHANNEL_ID,
        "photo": image_url,
        "caption": caption,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    response = requests.post(url, json=payload)
    return response.json()

# ==================================================
# ৭. মেইন ফাংশন (সবকিছু একসাথে)
# ==================================================
def main():
    print("🚀 Starting Auto-Poster (Image Mandatory)...")
    
    # র্যান্ডম টপিক বাছাই
    topic = random.choice(TOPICS)
    print(f"📌 Selected Topic: {topic}")
    
    # AI দিয়ে টেক্সট তৈরি
    ai_text = generate_ai_content(topic)
    
    # ফুটার যোগ
    footer = create_footer()
    
    # HTML ফরম্যাটে পুরো পোস্ট (বোল্ড, ইমোজি)
    full_post = (
        f"<b>🚀 {topic.upper()} 🔥</b>\n\n"
        f"{ai_text}\n\n"
        f"{footer}"
    )
    
    # ছবি আনো (এটা কখনো খালি ফিরবে না)
    image_url = fetch_image_guaranteed(topic)
    print(f"🖼️ Final Image URL: {image_url[:50]}...")
    
    # চ্যানেলে পোস্ট করো
    result = send_post_to_channel(image_url, full_post)
    
    if result.get('ok'):
        print("✅ Posted Successfully with Image!")
    else:
        print(f"❌ Failed: {result}")
    
    print(f"📅 Posted at: {datetime.now()}")

if __name__ == "__main__":
    main()
