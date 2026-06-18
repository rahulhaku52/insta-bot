import os
import random
import requests
import urllib.parse
from datetime import datetime

# ==================================================
# ১. গিটহাব সিক্রেটস লোড করা
# ==================================================
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
UNSPLASH_API_KEY = os.environ.get('UNSPLASH_API_KEY')

if not all([BOT_TOKEN, CHANNEL_ID, GEMINI_API_KEY, UNSPLASH_API_KEY]):
    print("❌ ERROR: Secrets missing!")
    exit(1)

# ==================================================
# ২. টপিক লিস্ট
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
    "Cloud Computing Innovations"
]

# ==================================================
# ৩. কন্টেন্ট জেনারেট (Gemini AI)
# ==================================================
def generate_ai_content(topic):
    prompt = f"""Write a short, exciting, and highly engaging social media post (max 100 words) about "{topic}". 
    Make it sound like breaking tech news. Use emojis, proper line breaks, and an enthusiastic tone. 
    Output only plain text with emojis, no markdown."""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"⚠️ AI Error: {e}")
        return f"🔥 Big updates are coming in the world of {topic}! Stay ahead of the curve with the latest tech innovations. 🚀"

# ==================================================
# ৪. ছবি আনা (Unsplash + Pollinations ব্যাকআপ)
# ==================================================
def fetch_image_guaranteed(query):
    # ১. Unsplash চেষ্টা
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
    
    # ২. ব্যাকআপ: Pollinations.ai
    print("🔄 Generating AI image via Pollinations.ai...")
    image_prompt = f"futuristic {query} technology concept, clean design, 4k"
    encoded_prompt = urllib.parse.quote(image_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=600&nologo=true"

# ==================================================
# ৫. প্রফেশনাল ফুটার + বাটন তৈরি (নতুন আপডেট)
# ==================================================
def create_professional_footer():
    """
    প্রিমিয়াম লুকের জন্য ইউনিকোড বর্ডার + ফ্যাশনেবল টেক্সট
    """
    footer_text = (
        "\n\n"
        "╔══════════════════════════════════╗\n"
        "║   ✦ 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐖𝐄𝐁 𝐒𝐎𝐋𝐔𝐓𝐈𝐎𝐍𝐒 ✦   ║\n"
        "╠══════════════════════════════════╣\n"
        "║  🔥 Professional Design         ║\n"
        "║  ⚡ Fast Delivery               ║\n"
        "║  💡 100% Custom Code            ║\n"
        "╚══════════════════════════════════╝"
    )
    return footer_text

def create_inline_button():
    """
    টেলিগ্রামের ইনলাইন বাটন তৈরি করা (স্ক্রিনশটের মতো)
    """
    button = {
        "inline_keyboard": [
            [
                {
                    "text": "📩 Contact Me Now",
                    "url": "https://t.me/hacker_52"
                }
            ]
        ]
    }
    return button

# ==================================================
# ৬. টেলিগ্রামে পোস্ট পাঠানো (বাটনসহ)
# ==================================================
def send_post_to_channel(image_url, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    # ক্যাপশনে HTML ব্যবহার করছি (বোল্ড, ইটালিকের জন্য)
    payload = {
        "chat_id": CHANNEL_ID,
        "photo": image_url,
        "caption": caption,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "reply_markup": create_inline_button()  # <--- এই লাইনেই বাটন অ্যাড হচ্ছে!
    }
    
    response = requests.post(url, json=payload)
    return response.json()

# ==================================================
# ৭. মেইন ফাংশন
# ==================================================
def main():
    print("🚀 Starting Premium Auto-Poster...")
    
    # টপিক বাছাই
    topic = random.choice(TOPICS)
    print(f"📌 Topic: {topic}")
    
    # AI টেক্সট
    ai_text = generate_ai_content(topic)
    
    # প্রফেশনাল ফুটার (নতুন স্টাইল)
    footer = create_professional_footer()
    
    # HTML ফরম্যাটে পুরো পোস্ট তৈরি
    full_post = (
        f"<b>🚀 {topic.upper()} 🔥</b>\n\n"
        f"{ai_text}\n\n"
        f"{footer}"
    )
    
    # ছবি আনা
    image_url = fetch_image_guaranteed(topic)
    print(f"🖼️ Image ready")
    
    # চ্যানেলে পোস্ট (বাটন সহ)
    result = send_post_to_channel(image_url, full_post)
    
    if result.get('ok'):
        print("✅ Posted Successfully with Premium Style & Button!")
    else:
        print(f"❌ Failed: {result}")
    
    print(f"📅 Time: {datetime.now()}")

if __name__ == "__main__":
    main()
