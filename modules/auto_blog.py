import os
import json
from datetime import datetime

def build_static_blog(new_posts, config, docs_dir="docs"):
    """
    建立歐美極簡獨立部落格風格 (Indie BearBlog / Substack 風) 的全英文靜態網站，
    直接賺取美金聯盟分潤與 Gumroad 美金數位商品收入。
    """
    os.makedirs(docs_dir, exist_ok=True)
    posts_json_path = os.path.join(docs_dir, "posts.json")

    existing_posts = []
    if os.path.exists(posts_json_path):
        try:
            with open(posts_json_path, "r", encoding="utf-8") as f:
                existing_posts = json.load(f)
        except Exception:
            existing_posts = []

    all_posts = (new_posts + existing_posts)[:30]

    with open(posts_json_path, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    site_title = config.get("site_title", "Practical Picks & Field Notes")
    site_desc = config.get("site_description", "Just a personal log of software deals, durable everyday gear, and simple spreadsheets I actually use.")
    aff_url = os.environ.get("AFFILIATE_USD_URL") or config.get("affiliate_links", {}).get("primary_usd_affiliate", "https://frostbite1787.gumroad.com/l/fpbvvo")
    store_url = os.environ.get("GUMROAD_PRODUCT_URL") or config.get("affiliate_links", {}).get("gumroad_usd_store", "https://frostbite1787.gumroad.com/l/fpbvvo")
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    cards_html = ""
    for post in all_posts:
        cards_html += f"""
        <article class="post-item">
            <div class="post-meta">
                <span class="tag">{post.get('category', 'Field Notes')}</span>
                <span class="time">{post.get('date', updated_at)}</span>
            </div>
            <h2>{post.get('title', '')}</h2>
            <p>{post.get('summary', '')}</p>
            <div class="post-links">
                <a href="{post.get('affiliate_url', aff_url)}" target="_blank" rel="noopener" class="link-primary">Check current price / deal page &rarr;</a>
                <a href="{post.get('store_url', store_url)}" target="_blank" rel="noopener" class="link-secondary">Grab my Minimalist Budget Sheet ($5)</a>
            </div>
        </article>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_title}</title>
    <meta name="description" content="{site_desc}">
    <style>
        :root {{
            --bg: #fafaf9;
            --surface: #ffffff;
            --text: #1c1917;
            --muted: #78716c;
            --border: #e7e5e4;
            --accent: #0f766e;
            --accent-light: #f0fdfa;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.7;
        }}
        header {{
            max-width: 720px;
            margin: 0 auto;
            padding: 3.5rem 1.5rem 2rem;
            border-bottom: 1px solid var(--border);
        }}
        header h1 {{
            font-size: 1.7rem;
            font-weight: 700;
            color: #1c1917;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }}
        header p {{
            color: var(--muted);
            font-size: 0.98rem;
            margin-bottom: 1.2rem;
        }}
        .nav-links {{
            display: flex;
            gap: 0.8rem;
            flex-wrap: wrap;
            font-size: 0.88rem;
        }}
        .nav-links a {{
            color: var(--accent);
            text-decoration: none;
            font-weight: 600;
            padding: 0.35rem 0.75rem;
            background: var(--accent-light);
            border-radius: 6px;
        }}
        .container {{
            max-width: 720px;
            margin: 1.5rem auto;
            padding: 0 1.5rem;
        }}
        .post-item {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.2rem;
        }}
        .post-meta {{
            display: flex;
            gap: 0.8rem;
            align-items: center;
            font-size: 0.8rem;
            color: var(--muted);
            margin-bottom: 0.5rem;
        }}
        .tag {{
            background: #f5f5f4;
            color: #44403c;
            padding: 0.15rem 0.55rem;
            border-radius: 4px;
            font-weight: 600;
        }}
        .post-item h2 {{
            font-size: 1.15rem;
            margin-bottom: 0.55rem;
            color: #1c1917;
            font-weight: 600;
        }}
        .post-item p {{
            color: #44403c;
            font-size: 0.95rem;
            margin-bottom: 1.1rem;
        }}
        .post-links {{
            display: flex;
            gap: 1.2rem;
            flex-wrap: wrap;
            font-size: 0.88rem;
            border-top: 1px dashed var(--border);
            padding-top: 0.85rem;
        }}
        .link-primary {{
            color: var(--accent);
            font-weight: 600;
            text-decoration: none;
        }}
        .link-primary:hover {{ text-decoration: underline; }}
        .link-secondary {{
            color: var(--muted);
            text-decoration: none;
        }}
        .link-secondary:hover {{ color: var(--text); text-decoration: underline; }}
        footer {{
            max-width: 720px;
            margin: 3rem auto 2rem;
            padding: 1.5rem;
            color: var(--muted);
            font-size: 0.8rem;
            border-top: 1px solid var(--border);
        }}
    </style>
</head>
<body>
    <header>
        <h1>{site_title}</h1>
        <p>{site_desc}</p>
        <div class="nav-links">
            <a href="{aff_url}" target="_blank" rel="noopener">Current Software & Game Bundles</a>
            <a href="{store_url}" target="_blank" rel="noopener">Download My Subscription Audit Sheet ($5)</a>
        </div>
    </header>
    <main class="container">
        {cards_html}
    </main>
    <footer>
        <p>Last updated: {updated_at}</p>
        <p style="margin-top:0.3rem;">Reader note: A few links on this page are referral links. If you grab something through them, I might get a couple bucks for coffee at no extra cost to you. Never buy stuff just because it's on sale.</p>
    </footer>
</body>
</html>"""

    index_path = os.path.join(docs_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)
