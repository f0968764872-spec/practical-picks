import os
from datetime import datetime

def generate_digital_products(posts, products_dir="products"):
    """
    產生可直接上架到 Gumroad / Lemon Squeezy / Etsy 賣給歐美網友的美金數位商品 ($5.99 USD ≈ 190 台幣)。
    只要全世界每天有 1 個人買，當天的台灣餐費就直接達標！
    """
    os.makedirs(products_dir, exist_ok=True)

    csv_path = os.path.join(products_dir, "2026_Minimalist_Budget_and_Subscription_Tracker_US.csv")
    csv_content = """\ufeffDate,Category,Item / Service,Monthly Cost (USD),Action Taken,Annual Savings (USD),Notes
2026-11-01,Subscriptions,Unused Streaming Service,15.99,Canceled,191.88,Switched to rotating one service at a time
2026-11-02,Software,Cloud Storage & Backup Tool,9.99,Switched to Lifetime Deal,119.88,Grabbed a one-time bundle deal instead of monthly billing
2026-11-03,Everyday Gear,Anker Braided USB-C 2-Pack,18.99,Bought on 40% Price Drop,11.40,Checked price history on CamelCamelCamel first
2026-11-04,Side Income,Gumroad Spreadsheet Download,0.00,Sold 1 Copy (+5.99 USD),0.00,Shared link in my personal notes page
"""
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(csv_content)

    md_path = os.path.join(products_dir, "The_No_BS_Productivity_and_Deal_Hunting_Playbook.md")
    latest_notes = "\n".join([f"- **{p.get('title')}**: {p.get('summary')}" for p in posts]) if posts else "- Updated weekly with price-checked software and durable everyday gear."

    md_content = f"""# The No-BS Subscription & Deal-Hunting Playbook (2026 Edition)

> Why I made this: Most budgeting templates have 40 tabs, broken macros, and charts nobody ever looks at after day three. I built this simple 1-page system for myself to track recurring subscriptions, spot fake discounts, and save an extra $150–$300 a month without living like a monk.

---

## 1. The "48-Hour Cart Rule" That Saved Me $1,200 Last Year

Whenever I see a piece of gear, software, or game on sale:
1. I put it in the cart or bookmark it.
2. I close the tab and wait 48 hours.
3. Roughly 80% of the time, I completely forget about it—which means I didn't actually need it.

---

## 2. Recent Deal Notes & Price Checks (Updated {datetime.now().strftime("%Y-%m-%d")})

{latest_notes}
"""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
