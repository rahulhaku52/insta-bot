import os
import json
import random
import requests
import urllib.parse
from datetime import datetime

# ==================================================
# UNICODE FONT STYLE HELPERS
# ==================================================

def to_bold_serif(text):
    """𝐋𝐢𝐤𝐞 𝐭𝐡𝐢𝐬 — Bold Serif for heading"""
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    bold   = '𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗'
    result = ''
    for ch in text:
        idx = normal.find(ch)
        result += bold[idx] if idx != -1 else ch
    return result

def to_italic_serif(text):
    """𝘓𝘪𝘬𝘦 𝘵𝘩𝘪𝘴 — Italic Serif for subtext / labels"""
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    italic = '𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻'
    result = ''
    for ch in text:
        idx = normal.find(ch)
        result += italic[idx] if idx != -1 else ch
    return result

def to_monospace(text):
    """𝚃𝚢𝚙𝚎 𝚕𝚒𝚔𝚎 𝚝𝚑𝚒𝚜 — Monospace for footer / code feel"""
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    mono   = '𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿'
    result = ''
    for ch in text:
        idx = normal.find(ch)
        result += mono[idx] if idx != -1 else ch
    return result

def to_double_struck(text):
    """𝕃𝕚𝕜𝕖 𝕥𝕙𝕚𝕤 — Double Struck for brand name"""
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    ds     = '𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡'
    result = ''
    for ch in text:
        idx = normal.find(ch)
        result += ds[idx] if idx != -1 else ch
    return result

def to_bold_italic(text):
    """𝙇𝙞𝙠𝙚 𝙩𝙝𝙞𝙨 — Bold Italic Sans for topic label"""
    normal    = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    bold_ital = '𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯'
    result = ''
    for ch in text:
        idx = normal.find(ch)
        result += bold_ital[idx] if idx != -1 else ch
    return result

# ==================================================
# ১. সিক্রেটস লোড
# ==================================================
BOT_TOKEN       = os.environ.get('BOT_TOKEN')
CHANNEL_ID      = os.environ.get('CHANNEL_ID')
NEWS_API_KEY    = os.environ.get('NEWS_API_KEY')
GEMINI_API_KEY  = os.environ.get('GEMINI_API_KEY')
UNSPLASH_API_KEY = os.environ.get('UNSPLASH_API_KEY')

if not all([BOT_TOKEN, CHANNEL_ID, NEWS_API_KEY, GEMINI_API_KEY]):
    print("❌ ERROR: Required env variables missing!")
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
# ২. নিউজ ফেচ
# ==================================================
def fetch_trending_topic():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": (
            '("web development" OR "app development" OR software OR programming '
            'OR React OR Python OR JavaScript OR Flutter OR API OR "frontend" '
            'OR "backend" OR "full stack") '
            '-cricket -football -politics -AI -Claude -Gemini'
        ),
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 8,
        "apiKey": NEWS_API_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=20)
        data = resp.json()
        if data.get('status') == 'ok':
            for art in data.get('articles', []):
                title = art.get('title', '')
                if '[Removed]' in title or not title:
                    continue
                clean = title.split('-')[0].strip()
                clean = clean.split('|')[0].strip()
                return clean
        else:
            print(f"API Error: {data.get('message')}")
    except Exception as e:
        print(f"Fetch Error: {e}")

    return "Latest Web Development Frameworks in 2026"

# ==================================================
# ৩. Gemini AI Content
# ==================================================
def generate_ai_content(topic):
    prompt = f"""Write a short, professional, and insightful tech news update \
(70-90 words) about: "{topic}".
Write in a clear journalistic style with 2 short paragraphs.
No emojis, no hashtags. Polished tone like Wired or TechCrunch.
Output only plain text."""

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    )
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        resp = requests.post(url, json=payload, timeout=30)
        data = resp.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"⚠️ Gemini Error: {e}")
        return (
            f"Developers are exploring new possibilities in {topic}. "
            "This shift is shaping modern software architecture and improving "
            "developer productivity across the board."
        )

# ==================================================
# ৪. ইমেজ ফেচ
# ==================================================
def fetch_image_guaranteed(query):
    if UNSPLASH_API_KEY:
        url = (
            f"https://api.unsplash.com/photos/random"
            f"?query={query}&orientation=landscape&count=1"
        )
        headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list) and data:
                    print("✅ Image from Unsplash")
                    return data[0]['urls']['regular']
        except Exception as e:
            print(f"⚠️ Unsplash Error: {e}")

    print("🔄 Using Pollinations fallback...")
    prompt  = "modern web development coding technology clean design"
    encoded = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1200&height=600&nologo=true"

# ==================================================
# ৫. 🎨 PREMIUM POST FORMAT — Multi Font Style
# ==================================================
def format_premium_post(topic, ai_text):
    """
    ✦  Brand name      → Double Struck  𝕳𝖆𝖐𝖚
    ✦  Section label   → Italic Serif   𝘛𝘰𝘥𝘢𝘺'𝘴 𝘛𝘰𝘱𝘪𝘤
    ✦  Topic heading   → Bold Serif     𝐋𝐢𝐤𝐞 𝐭𝐡𝐢𝐬
    ✦  Body text       → Plain / normal
    ✦  Footer label    → Bold Italic    𝙃𝙖𝙠𝙪
    ✦  Footer contact  → Monospace      𝚌𝚘𝚍𝚎 𝚜𝚝𝚢𝚕𝚎
    """

    # ── Brand ──────────────────────────────────────
    brand    = to_double_struck("HAKU DEV")      # 𝕳𝕬𝕶𝕌 𝔻𝔼𝕍
    divider  = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # ── Topic label ────────────────────────────────
    label    = to_italic_serif("Todays Topic")   # 𝘛𝘰𝘥𝘢𝘺𝘴 𝘛𝘰𝘱𝘪𝘤

    # ── Heading (topic) ────────────────────────────
    heading  = to_bold_serif(topic)              # 𝐁𝐨𝐥𝐝 𝐒𝐞𝐫𝐢𝐟

    # ── Footer ─────────────────────────────────────
    by_label = to_bold_italic("by Haku")         # 𝙗𝙮 𝙃𝙖𝙠𝙪
    contact  = to_monospace("@hacker_52")        # 𝚌𝚘𝚍𝚎 𝚕𝚘𝚘𝚔
    dev_tag  = to_monospace("Web & App Dev")

    lines = [
        "",
        f"✦  {brand}  ✦",
        "",
        divider,
        "",
        f"◈  {label}",
        "",
        heading,
        "",
        ai_text.strip(),
        "",
        divider,
        "",
        f"✉  {contact}   {dev_tag}",
        f"   {by_label}",
        "",
    ]

    return "\n".join(lines)

# ==================================================
# ৬. Inline Button
# ==================================================
def create_inline_button():
    return {
        "inline_keyboard": [[
            {"text": "📩 Connect with Haku", "url": "https://t.me/hacker_52"}
        ]]
    }

# ==================================================
# ৭. টেলিগ্রামে পোস্ট
# ==================================================
def send_photo_post(image_url, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id":                  CHANNEL_ID,
        "photo":                    image_url,
        "caption":                  caption,
        "parse_mode":               "HTML",
        "disable_web_page_preview": True,
        "reply_markup":             create_inline_button()
    }
    return requests.post(url, json=payload)

# ==================================================
# ৮. Main
# ==================================================
def main():
    print("🚀 Haku DEV Bot starting...")

    raw_topic = fetch_trending_topic()
    topic     = raw_topic[:80]

    posted = load_posted()
    if topic in posted:
        print(f"📭 Already posted: {topic}. Skipping.")
        return

    print(f"📌 Topic: {topic}")

    ai_text   = generate_ai_content(topic)
    caption   = format_premium_post(topic, ai_text)
    image_url = fetch_image_guaranteed("web development coding")

    print("\n── Preview ──────────────────────────")
    print(caption)
    print("─────────────────────────────────────\n")

    result = send_photo_post(image_url, caption)

    if result.status_code == 200:
        posted.add(topic)
        save_posted(posted)
        print("✅ Posted successfully!")
    else:
        print(f"❌ Failed: {result.text}")

if __name__ == "__main__":
    main()
