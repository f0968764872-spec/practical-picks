import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

def fetch_trending_items(limit=3):
    """
    從歐美高轉換率的公開 RSS (Reddit r/GameDeals, HackerNews) 抓取最新折扣與實用工具。
    """
    items = []
    rss_urls = [
        "https://www.reddit.com/r/GameDeals/new/.rss",
        "https://hnrss.org/frontpage?points=120"
    ]
    for url in rss_urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=8) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                for elem in root.iter():
                    tag = elem.tag.split('}')[-1]
                    if tag in ('item', 'entry'):
                        title = ""
                        link = ""
                        for child in elem:
                            ctag = child.tag.split('}')[-1]
                            if ctag == 'title' and child.text:
                                title = child.text.strip()
                            elif ctag == 'link':
                                link = child.text.strip() if child.text else child.attrib.get('href', '')
                        if title and link:
                            items.append({"raw_title": title, "source_url": link})
                        if len(items) >= limit:
                            break
        except Exception:
            pass
        if len(items) >= limit:
            break

    if not items:
        items = [
            {
                "raw_title": "Humble Tech & Indie PC Bundle - 85% off DRM-free tools and games",
                "source_url": "https://www.humblebundle.com/"
            },
            {
                "raw_title": "Anker 100W Braided USB-C Cable 2-Pack & GaN Wall Charger Price Drop",
                "source_url": "https://www.amazon.com/"
            },
            {
                "raw_title": "Open-source local file converter & subscription audit spreadsheet",
                "source_url": "https://gumroad.com/"
            }
        ]
    return items[:limit]


def generate_ai_affiliate_posts(raw_items, config):
    """
    產生 100% 道地美國 Reddit 鄉民口吻 (r/Frugal, r/BuyItForLife, r/GameDeals) 的英文分享文。
    完全禁止 ChatGPT 常見單字 (delve, game-changer, testament, elevate, unlock, look no further) 與罐頭表情符號。
    """
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    aff_url = (
        os.environ.get("AFFILIATE_USD_URL")
        or config.get("affiliate_links", {}).get("primary_usd_affiliate", "https://frostbite1787.gumroad.com/l/fpbvvo")
    )
    store_url = (
        os.environ.get("GUMROAD_PRODUCT_URL")
        or config.get("affiliate_links", {}).get("gumroad_usd_store", "https://frostbite1787.gumroad.com/l/fpbvvo")
    )

    human_us_templates = [
        {
            "title_fmt": "Quick heads-up on this price drop: {topic}",
            "category": "Deal Check",
            "summary_fmt": "I've had this bookmarked for a couple months waiting for a decent discount. Checked the price history this morning and it's finally down to a reasonable number. Probably not worth it at full retail, but at this price it's a solid pickup if you actually need one.",
            "social_fmt": "Just noticed {topic} dropped in price today.\n\nBeen using a similar setup for about six months without any issues. Definitely don't impulse-buy it if you don't need it, but if it was already on your wishlist, now's a good time.\n\nDeal link: {aff_url}\nMy simple subscription & budget sheet: {store_url}",
            "shorts_fmt": "Honestly, I usually skip these sales because half the time they mark the price up right before discounting it. But I checked the six-month price graph on {topic} this morning, and it's actually at a legit low right now. If you've been holding off on grabbing it, I put the direct link and my price-tracking sheet in my bio."
        },
        {
            "title_fmt": "Tested a few options for {topic} — here's what stuck",
            "category": "Field Notes",
            "summary_fmt": "Spent way too much time last weekend comparing different setups on Reddit before settling on this one. No flashy gimmicks or annoying monthly subscriptions—it just works the way it's supposed to.",
            "social_fmt": "Figured I'd share my notes on {topic} since a few people asked.\n\nTried two other options earlier this year that felt super clunky. This one has been solid so far and saved me a couple hours a week.\n\nCheck it out here: {aff_url}\nMy no-BS budget tracker ($5): {store_url}",
            "shorts_fmt": "I don't know who needs to hear this, but stop paying fifteen bucks a month for basic tools you can get once and own forever. I switched over to {topic} a few weeks ago and haven't looked back. It's super straightforward, no bloat, and saves a ton of money over a year. Link is in the bio if you want to check it out."
        },
        {
            "title_fmt": "Small weekend win: {topic}",
            "category": "Frugal Picks",
            "summary_fmt": "With everything getting more expensive lately, I've been doing a strict audit on random everyday purchases. This is one of the few under-$20 pickups from the last few months that genuinely earned its spot on my desk.",
            "social_fmt": "Doing my monthly expense audit and realized how much money I used to waste on overpriced gear.\n\nSwitched to {topic} recently and it does the exact same job for a fraction of the cost.\n\nLink if you're curious: {aff_url}\nThe spreadsheet I use to track recurring bills: {store_url}",
            "shorts_fmt": "Every couple months I go through my bank statement just to see what sneaky subscriptions or overpriced stuff I can cut. One of the easiest swaps I made recently was grabbing {topic} while it was on sale. Does the exact same job as the expensive ones for way less. I left the link and my subscription audit sheet in my bio."
        }
    ]

    processed_posts = []

    for idx, item in enumerate(raw_items):
        raw_title = item["raw_title"]
        source_url = item["source_url"]

        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"""
Write like a real American Reddit user on r/Frugal, r/BuyItForLife, or r/GameDeals sharing a note about: "{raw_title}".
STRICT ANTI-AI RULES:
1. NEVER use words like: delve, testament, game-changer, unlock, elevate, seamlessly, beacon, buckle up, look no further, in today's fast-paced world.
2. NO emoji spam. Use 0 emojis.
3. Keep the tone understated, practical, slightly skeptical of marketing hype, and casual (like a real human writing a quick note to friends). Even remind people "don't buy it if you don't actually need it."

Output ONLY raw JSON (no markdown backticks) with these keys:
- "title": Casual human title (under 12 words, no emojis)
- "category": Short label ("Deal Check", "Field Notes", or "Frugal Picks")
- "summary": 2-3 natural sentences explaining why it's decent value
- "telegram_text": A short post for Reddit/X/Telegram/Discord including {aff_url} and {store_url}
- "shorts_script": 30-second spoken American English voiceover script (around 75-90 words, conversational, zero hype)
"""
                response = model.generate_content(prompt)
                text = response.text.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
                data = json.loads(text)
                data["affiliate_url"] = aff_url
                data["store_url"] = store_url
                data["source_url"] = source_url
                data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
                processed_posts.append(data)
                continue
            except Exception:
                pass

        tpl = human_us_templates[idx % len(human_us_templates)]
        short_topic = raw_title[:48]
        processed_posts.append({
            "title": tpl["title_fmt"].format(topic=short_topic),
            "category": tpl["category"],
            "summary": tpl["summary_fmt"].format(topic=short_topic),
            "telegram_text": tpl["social_fmt"].format(topic=short_topic, aff_url=aff_url, store_url=store_url),
            "shorts_script": tpl["shorts_fmt"].format(topic=short_topic),
            "affiliate_url": aff_url,
            "store_url": store_url,
            "source_url": source_url,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

    return processed_posts


def push_to_channels(posts):
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    tg_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    discord_webhook = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()

    for post in posts:
        msg = post["telegram_text"]
        if tg_token and tg_chat_id:
            try:
                url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
                payload = json.dumps({"chat_id": tg_chat_id, "text": msg}).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(req, timeout=10)
            except Exception:
                pass
        if discord_webhook:
            try:
                payload = json.dumps({"content": msg}).encode("utf-8")
                req = urllib.request.Request(discord_webhook, data=payload, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
                urllib.request.urlopen(req, timeout=10)
            except Exception:
                pass
