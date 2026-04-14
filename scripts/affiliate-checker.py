#!/usr/bin/env python3
"""
殺手林 申請Affiliate大作戰
================================
自動申請各大聯盟計劃

每個平台都有不同的 commission 結構：
- Amazon Associates: 3-10% (取決於產品類別)
- Teachable: 30% recurring
- Notion: 50% of first year ($50 max)
- Gumroad: 30% of your own products
- Canva: 30% of Pro/year plans

用法:
  python3 affiliate_applier.py --list     # 列出所有可申請的平台
  python3 affiliate_applier.py --apply     # 申請所有平台
  python3 affiliate_applier.py --status    # 檢查申請狀態
"""
import json
import os
from datetime import datetime

# ====== AFFILIATE PROGRAMS ======
PROGRAMS = [
    {
        "name": "Gumroad Creator Affiliate",
        "url": "https://gumroad.com/affiliates",
        "commission": "30% of all Gumroad sales you refer",
        "cookie": "N/A (Gumroad uses direct links)",
        "note": "You promote YOUR OWN Gumroad products. Earn 30% when someone buys through your link.",
        "products": "All 7 products on linblance.gumroad.com",
        "signup_url": "https://gumroad.com/affiliates"
    },
    {
        "name": "Amazon Associates",
        "url": "https://affiliate-program.amazon.com",
        "commission": "3-10% depending on category",
        "cookie": "24 hours",
        "note": "Promote books, tools, courses related to entrepreneurship. Best for niche sites.",
        "products": "Books on I Ching, entrepreneurship, business strategy",
        "signup_url": "https://affiliate-program.amazon.com/signup"
    },
    {
        "name": "Teachable Affiliate",
        "url": "https://teachable.com/affiliates",
        "commission": "30% recurring (first payment + every renewal)",
        "cookie": "30 days",
        "note": "Promote online courses. If your audience buys courses, this pays 30% recurring.",
        "products": "Business courses, productivity courses, I Ching courses",
        "signup_url": "https://teachable.com/affiliates"
    },
    {
        "name": "Notion Affiliate",
        "url": "https://www.notion.so/affiliates",
        "commission": "50% of first year revenue ($50 max per sale)",
        "cookie": "30 days",
        "note": "Notion Teams/Plus subscriptions. $8/month or $96/year per referral.",
        "products": "Notion templates, productivity tools",
        "signup_url": "https://www.notion.so/affiliates"
    },
    {
        "name": "Canva Affiliate",
        "url": "https://www.canva.com/affiliates/",
        "commission": "30% of Pro subscription first year",
        "cookie": "30 days",
        "note": "Canva Pro is $119.99/year. 30% = ~$36 per sale.",
        "products": "Design tools, graphic templates",
        "signup_url": "https://www.canva.com/affiliates/"
    },
    {
        "name": "Readwise Affiliate",
        "url": "https://readwise.io/affiliates",
        "commission": "30% recurring",
        "cookie": "30 days",
        "note": "Readwise Reader + Highlights. Popular among readers and learners.",
        "products": "Reading/note-taking tools",
        "signup_url": "https://readwise.io/affiliates"
    },
    {
        "name": "Todoist Affiliate",
        "url": "https://todoist.com/affiliates",
        "commission": "30% first year",
        "cookie": "30 days",
        "note": "Todoist Pro is $48/year. Good for productivity niche.",
        "products": "Task management, productivity",
        "signup_url": "https://todoist.com/affiliates"
    },
    {
        "name": "Reclaim Affiliate",
        "url": "https://reclaim.ai/affiliates",
        "commission": "30% first year",
        "cookie": "30 days",
        "note": "AI calendar assistant. Popular among entrepreneurs.",
        "products": "AI productivity tools",
        "signup_url": "https://reclaim.ai/affiliates"
    },
    {
        "name": "Framer Affiliate",
        "url": "https://www.framer.com/affiliates/",
        "commission": "25% recurring",
        "cookie": "30 days",
        "note": "Website builder. Framer is popular for portfolios and startups.",
        "products": "Website building, design tools",
        "signup_url": "https://www.framer.com/affiliates/"
    },
    {
        "name": "LemonSqueezy Affiliate",
        "url": "https://www.lemonsqueezy.com/affiliates",
        "commission": "30% recurring",
        "cookie": "90 days (best!)",
        "note": "Digital product platform. Alternative to Gumroad.",
        "products": "Digital products, SaaS",
        "signup_url": "https://www.lemonsqueezy.com/affiliates"
    }
]

APPLIED_FILE = "/Users/lingo/.openclaw/workspace/shaishalin/data/affiliate-applications.json"

def load_applications():
    os.makedirs(os.path.dirname(APPLIED_FILE), exist_ok=True)
    if os.path.exists(APPLIED_FILE):
        with open(APPLIED_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_applications(apps):
    with open(APPLIED_FILE, 'w') as f:
        json.dump(apps, f, ensure_ascii=False, indent=2)

def mark_applied(name):
    apps = load_applications()
    apps[name] = {
        "applied_at": datetime.now().isoformat(),
        "status": "applied",
        "note": ""
    }
    save_applications(apps)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='殺手林 申請Affiliate大作戰')
    parser.add_argument('--list', action='store_true', help='列出所有可申請的平台')
    parser.add_argument('--apply', type=str, metavar='NAME', help='申請指定平台（名稱）')
    parser.add_argument('--status', action='store_true', help='檢查申請狀態')
    parser.add_argument('--applied', action='store_true', help='顯示已申請的平台')
    args = parser.parse_args()
    
    if args.list:
        print("\n📋 殺手林 Affiliate 申請清單\n")
        print("=" * 70)
        apps = load_applications()
        for i, prog in enumerate(PROGRAMS, 1):
            status = "✅ 已申請" if prog['name'] in apps else "⏳ 可申請"
            print(f"\n{i}. {prog['name']} {status}")
            print(f"   💰 {prog['commission']}")
            print(f"   🍪 {prog['cookie']}")
            print(f"   🔗 {prog['signup_url']}")
            print(f"   📝 {prog['note']}")
        print("\n" + "=" * 70)
    
    elif args.apply:
        name = args.apply
        found = [p for p in PROGRAMS if name.lower() in p['name'].lower()]
        if found:
            prog = found[0]
            mark_applied(prog['name'])
            print(f"✅ 已記錄申請：{prog['name']}")
            print(f"   請到以下網址完成申請：")
            print(f"   🔗 {prog['signup_url']}")
        else:
            print(f"❌ 找不到：{name}")
            print("   使用 --list 查看所有平台")
    
    elif args.applied:
        apps = load_applications()
        print(f"\n✅ 已申請的 Affiliate 平台 ({len(apps)}):\n")
        for name, data in apps.items():
            print(f"  - {name}")
            print(f"    申請時間: {data.get('applied_at', 'unknown')}")
            print(f"    狀態: {data.get('status', 'unknown')}")
            print()
    
    elif args.status:
        apps = load_applications()
        print(f"\n📊 Affiliate 申請狀態 ({len(apps)} 已申請 / {len(PROGRAMS)} 總數)\n")
        for prog in PROGRAMS:
            if prog['name'] in apps:
                print(f"✅ {prog['name']}")
            else:
                print(f"⏳ {prog['name']}")
    
    else:
        print("殺手林 Affiliate 申請大作戰")
        print("用法:")
        print("  --list     列出所有可申請的平台")
        print("  --apply   申請指定平台")
        print("  --status  檢查申請狀態")
        print("  --applied 顯示已申請的平台")
        print()
        print("範例:")
        print("  python3 affiliate_applier.py --list")
        print("  python3 affiliate_applier.py --apply 'Amazon'")
        print("  python3 affiliate_applier.py --apply 'Teachable'")

if __name__ == '__main__':
    main()
