import os
import json
from modules.affiliate_bot import fetch_trending_items, generate_ai_affiliate_posts, push_to_channels
from modules.auto_blog import build_static_blog
from modules.shorts_generator import build_daily_shorts
from modules.digital_product_maker import generate_digital_products

def main():
    print("====================================================")
    print("🚀 啟動【四合一 AI 全自動被動收入矩陣系統】")
    print("====================================================")

    config_path = "config.json"
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

    limit = config.get("post_count_per_run", 3)

    # 1. 抓取最新情報 + AI 生成推坑文與分潤連結 (方案一)
    print("\n[步驟 1/4] 正在抓取全網最新熱門情報並生成 AI 聯盟行銷推坑文...")
    raw_items = fetch_trending_items(limit=limit)
    posts = generate_ai_affiliate_posts(raw_items, config)
    push_to_channels(posts)

    # 2. 自動更新 SEO 利基型情報網站 (方案二)
    print("\n[步驟 2/4] 正在自動建置/更新 GitHub Pages 情報與分潤網站...")
    build_static_blog(posts, config, docs_dir="docs")

    # 3. 自動生成 30 秒無臉短影音配音、字幕與影片 (方案三)
    print("\n[步驟 3/4] 正在生成今日無臉短影音腳本、AI 語音與字幕...")
    build_daily_shorts(posts, config, output_dir="output_shorts")

    # 4. 自動生成可販售數位商品與模板 (方案四)
    print("\n[步驟 4/4] 正在更新可販售數位商品模板庫...")
    generate_digital_products(posts, products_dir="products")

    print("\n✅ 四合一自動化流水線執行完畢！")

if __name__ == "__main__":
    main()

