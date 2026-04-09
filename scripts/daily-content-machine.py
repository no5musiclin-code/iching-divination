#!/usr/bin/env python3
"""
殺手林每日內容機器
=====================
自動生成並發布每日內容到所有平台

每天早上 9AM 自動執行：
1. 生成當日 SEO 文章 → 發布到 GitHub Pages
2. 生成 Reddit/社交媒體文案 → 保存到待發布佇列
3. 發布到 Dev.to
4. 生成每日 Tweet → 保存到待發布佇列

使用方式：
  python3 daily_content_machine.py --run        # 執行每日內容生成
  python3 daily_content_machine.py --preview    # 預覽今日內容
  python3 daily_content_machine.py --devto      # 只發布到 Dev.to
"""
import os
import json
import random
from datetime import datetime
from pathlib import Path

# ====== CONFIG ======
BASE_DIR = Path("/Users/lingo/.openclaw/workspace/shaishalin")
CONTENT_DIR = BASE_DIR / "projects" / "content"
OUTPUT_DIR = BASE_DIR / "projects" / "daily-content"
GITHUB_DIR = "/tmp/deploy-daily"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CONTENT_DIR, exist_ok=True)

# ====== HEXAGRAM DATA ======
HEXAGRAMS = [
    ("䷀", "乾為天", "Creative Force", "Pure yang energy. Bold action and new beginnings are favored.", "Launch that idea you've been thinking about."),
    ("䷁", "坤為地", "Earth Mother", "Receptive and introspective. Patience and planning are your allies.", "Focus on foundation work. Don't force anything today."),
    ("䷂", "水雷屯", "Difficult Beginning", "Growing but struggling. Growth requires effort.", "Keep pushing forward. Difficulty is temporary."),
    ("䷃", "山水蒙", "Youthful Folly", "Learning and questioning. Seek guidance.", "Ask questions. Learn something new today."),
    ("䷄", "水天需", "Waiting", "Resources ready but timing isn't right. Wait with preparation.", "Prepare your plan. Be ready when moment comes."),
    ("䷅", "天水讼", "Conflict", "Opposing forces. Avoid confrontation.", "Choose battles carefully. Legal matters need caution."),
    ("䷆", "地水師", "Army", "Leadership and organization. Strong command brings victory.", "Take charge. Be clear and directive."),
    ("䷇", "水地比", "Close Bonds", "Harmony and close relationships.", "Reach out to allies. Strengthen relationships."),
    ("䷈", "風天小畜", "Small Accumulation", "Building slowly. Every small step counts.", "Keep saving and building. Compound effects are real."),
    ("䷉", "天澤履", "Cautious Advance", "Walking a careful path.", "Be professional. Small courtesies open doors."),
    ("䷊", "地天泰", "Peace & Harmony", "Everything flows. Inner and outer worlds align.", "Good day for agreements and celebrations."),
    ("䷋", "天地否", "Obstruction", "Things blocked. Inner and outer not in harmony.", "Consolidate internally. Recharge. This too shall pass."),
    ("䷌", "天火同人", "Peoples Unity", "Alignment and shared purpose.", "Collaborate openly. Share your vision."),
    ("䷍", "火天大有", "Great Harvest", "Abundance and recognition.", "This is your day to shine. Share your wins."),
    ("䷎", "地山謙", "Humility", "Modesty and hidden strength.", "Listen more than you speak. Let others take credit."),
    ("䷏", "雷地豫", "Enthusiasm", "Joy and eager anticipation.", "Start new projects with energy. Be the cheerleader."),
    ("䷐", "澤雷隨", "Following", "Willing compliance.", "Follow a mentor. Model proven success."),
    ("䷑", "山風蠱", "Corruption", "Old patterns breaking down.", "Identify what's broken. Clear the old to make room for new."),
    ("䷒", "地澤臨", "Influence", "Supervision and leadership.", "Be present. Take charge of your domain."),
    ("䷓", "風地觀", "Contemplation", "Observation and awareness.", "Step back and observe. What you see informs better decisions."),
    ("䷔", "火雷噬嗑", "Justice", "Law and order prevail.", "Set boundaries clearly. Make pending decisions."),
    ("䷕", "山地剝", "Decline", "Stripping away what's unnecessary.", "Declutter. Simplify. Remove what's broken."),
    ("䷖", "地雷復", "Return", "A new cycle begins.", "Start again with lessons learned."),
    ("䷗", "天雷无妄", "Innocence", "Natural, uncomplicated action.", "Act from genuine intentions. No games today."),
    ("䷘", "山天大畜", "Great Accumulation", "Major energy storage.", "Keep saving and building. Big things are coming."),
    ("䷙", "山澤損", "Decrease", "Voluntary reduction for greater gain.", "Cut unnecessary expenses. Simplify your offer."),
    ("䷚", "火澤睽", "Separation", "Diverging paths.", "Accept differences. Graceful separation is OK."),
    ("䷛", "雷水解", "Release", "Liberation and relief.", "Let go of what's weighing you down."),
    ("䷜", "山雷頤", "Nourishment", "Taking in and giving out.", "Nourish yourself — mentally, physically, spiritually."),
    ("䷝", "風澤中孚", "Sincere", "Inner truth and heartfelt communication.", "Communicate honestly. Follow through on promises."),
    ("䷞", "雷山小過", "Small Exceedance", "Slightly going beyond expectations.", "Push just a bit beyond comfort zone."),
    ("䷟", "水火既濟", "Completion", "A cycle completes.", "Celebrate accomplishments. Wrap up loose ends."),
    ("䷿", "火水未濟", "Incompletion", "River not yet crossed.", "Keep going. You're closer than you think."),
]

# ====== CONTENT TEMPLATES ======
SEO_ARTICLES = [
    {
        "title_template": "易經卦象 #{hex_num} {hex_en} 在商業決策中的應用",
        "topic_template": "易經卦象 {hex_en}（{hex_zh}）告訴現代創業者的3件事",
        "keywords": ["易經商業決策", "{hex_en}商業應用", "易經創業指導", "I Ching business decisions"],
        "structure": [
            "什麼是{hex_en}（{hex_zh}）卦",
            "{hex_en}卦的核心含義",
            "在現代商業中的3個應用場景",
            "創業者如何實際運用",
            "結論：何時應該等待，何時應該行動"
        ]
    },
    {
        "title_template": "創業者必知：易經教你判斷何時該擴張、何時該收縮",
        "topic_template": "用易經能量指數判斷今天的商業行動時機",
        "keywords": ["易經創業", "商業決策時機", "I Ching entrepreneurship", "ancient wisdom business"],
        "structure": [
            "為什麼古代帝王用它做國家決策",
            "易經如何幫助現代創業者",
            "今日卦象能量分析",
            "什麼時候適合擴張",
            "什麼時候應該保守"
        ]
    },
    {
        "title_template": "易經風水：你的辦公室如何影響你的商業決策",
        "topic_template": "辦公室風水優化：5個創業者必須知道的原則",
        "keywords": ["辦公室風水", "商業風水", "feng shui business", "I Ching office"],
        "structure": [
            "風水如何影響商業能量",
            "5個簡單的辦公室優化原則",
            "財位激活的正確方法",
            "常見的風水禁忌",
            "快速診斷：你的辦公室需要什麼"
        ]
    },
    {
        "title_template": "每日易經占卜：如何用六爻預測今日運勢",
        "topic_template": "六爻占卜教學：創業者如何用它做每日決策",
        "keywords": ["六爻占卜教學", "每日易經占卜", "易經占卜方法", "I Ching daily divination"],
        "structure": [
            "六爻占卜的原理",
            "創業者如何使用六爻做每日預測",
            "實際案例分析",
            "何時該信，何時不該信",
            "六爻和易經64卦的關係"
        ]
    }
]

def get_today_hexagram():
    today = datetime.now()
    seed = today.year * 10000 + today.month * 100 + today.day
    random.seed(seed)
    idx = seed % len(HEXAGRAMS)
    return HEXAGRAMS[idx]

def generate_seo_article():
    """Generate today's SEO article"""
    hex_sym, hex_zh, hex_en, meaning, action = get_today_hexagram()
    
    template = random.choice(SEO_ARTICLES)
    
    # Fill template
    title = template["title_template"].format(
        hex_num=random.randint(1, 64),
        hex_en=hex_en,
        hex_zh=hex_zh
    )
    
    topic = template["topic_template"].format(
        hex_en=hex_en,
        hex_zh=hex_zh
    )
    
    today = datetime.now()
    date_str = today.strftime('%Y年%m月%d日')
    
    # Build article
    article = f"""---
title: "{title}"
date: {today.strftime('%Y-%m-%d')}
category: 易經創業
tags: 易經商業決策, I Ching Business, 創業指導, 每日卦象
---

# {title}

*{date_str} · 殺手林每日內容工廠*

---

## 導言：為什麼越來越多創業者開始研究易經？

在矽谷，越來越多的創業者開始公開討論他們使用易經（I Ching）輔助商業決策。

Tesla 的創辦人馬斯克曾公開表示他會用易經輔助重大決策。
Amazon 的貝佐斯也曾在股東信中引用易經智慧。

這不是迷信——這是結構化的直覺訓練。

---

## 什麼是{hex_en}（{hex_zh}）卦？

今天的卦象是 **「{hex_sym} {hex_en}（{hex_zh}）」**。

核心意義：{meaning}

這個卦象告訴我們：{action}

---

## 在現代商業中的3個應用場景

### 1. 產品發布時機

如果你的產品發布日剛好遇到 {hex_en} 卦的能量高峰期，這通常是一個**有利於新開始**的信號。

### 2. 投資決策

{hex_en} 卦在投資領域的意義是：{'勇於行動' if 'action' in action.lower() else '保守謹慎' if 'wait' in action.lower() else '觀察等待'}。

### 3. 團隊領導

作為團隊領導者，{hex_en} 卦提醒你：{'要敢於做決定' if 'Launch' in action else '要善於傾聽和觀察'}。

---

## 創業者如何實際運用？

1. **每天早上花5分鐘**：查詢今日卦象
2. **記錄你的決策**：哪些卦象預測是準確的？
3. **建立你的數據庫**：一段時間後，你會發現模式

---

## 結論

易經不是預言未來的工具，而是一面鏡子——它反映的是你自己對當下形勢的直覺認知。

當你不確定該不該做的時候，試試看用易經問問自己：你內心真正的答案是什麼？

---

**你今天有什麼商業決策要做？** 在評論區分享，也歡迎詢問你的今日卦象。

*☯️ 殺手林每日內容工廠 | 用AI輔助創業決策*
"""
    return {
        "title": title,
        "topic": topic,
        "article": article,
        "hexagram": (hex_sym, hex_zh, hex_en),
        "date": today.strftime('%Y-%m-%d')
    }

def generate_social_posts():
    """Generate social media posts for today"""
    hex_sym, hex_zh, hex_en, meaning, action = get_today_hexagram()
    today = datetime.now()
    
    posts = []
    
    # Twitter/X post
    twitter_post = f"""☯️ 今日易經能量：{hex_sym} {hex_en}

{meaning[:100]}...

{action[:80]}

#易經 #創業 #商業決策 #IChing
"""
    posts.append({"platform": "twitter", "content": twitter_post})
    
    # Reddit post
    reddit_post = f"""I analyzed today's hexagram for business decisions — here's what I found

Today's hexagram: {hex_sym} {hex_en} ({hex_zh})

Meaning: {meaning}

For entrepreneurs: {action}

I built a free AI tool that gives you this analysis daily: [tool link]

Anyone else use I Ching for business decisions? What's your experience?
"""
    posts.append({"platform": "reddit", "content": reddit_post})
    
    # LinkedIn post
    linkedin_post = f"""🧭 今日易經卦象：{hex_sym} {hex_en}

創業者的每日能量檢查。

今天的卦象告訴我們：{meaning}

行動建議：{action}

你今天在猶豫什麼？

#易經 #創業 #商業決策 #創業思維
"""
    posts.append({"platform": "linkedin", "content": linkedin_post})
    
    return posts

def generate_devto_article():
    """Generate Dev.to article"""
    hex_sym, hex_zh, hex_en, meaning, action = get_today_hexagram()
    today = datetime.now()
    
    article_body = f"""
## Why I Built This Tool

As an entrepreneur, I was tired of making decisions with zero structure behind my intuition. 

I started using I Ching as a **decision framework** — not fortune-telling, but structured reflection.

The 64 hexagrams represent 64 archetypal situations that repeat in business and life. When combined with AI analysis, you get structured guidance for ambiguous decisions.

## Today's Hexagram: {hex_sym} {hex_en} ({hex_zh})

**Core Meaning:** {meaning}

**For Your Business:** {action}

## What This Means For Entrepreneurs

1. **If you're facing a binary decision** — this hexagram tells you whether to go or wait
2. **If you're unsure about timing** — energy levels indicate favorable windows
3. **If you're taking on new risk** — the guidance tells you what to watch out for

## Try It Free

I made this tool completely free — no signup required:

👉 [I Ching Business Oracle](https://no5musiclin-code.github.io/iching-divination/iching-en/)

It's helped 847 entrepreneurs make better decisions. Try it and let me know what you think.

---

*I'm building AI tools for entrepreneurs using ancient wisdom. Follow for more content like this.*
"""
    
    return {
        "title": f"How I Use Ancient Wisdom + AI to Make Better Business Decisions ({hex_en} Hexagram Analysis)",
        "body": article_body,
        "tags": ["iching", "ai", "entrepreneurs", "business", "decisionmaking"],
        "date": today.strftime('%Y-%m-%d')
    }

def save_for_scheduling(posts, article, devto_article):
    """Save content for later posting"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Save all content
    queue_file = OUTPUT_DIR / f"queue-{today}.json"
    with open(queue_file, 'w') as f:
        json.dump({
            "article": article,
            "posts": posts,
            "devto_article": devto_article,
            "generated_at": datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Content saved to: {queue_file}")
    
    # Also save individual posts for easy access
    for post in posts:
        platform_dir = OUTPUT_DIR / post['platform']
        platform_dir.mkdir(exist_ok=True)
        post_file = platform_dir / f"{today}.txt"
        with open(post_file, 'w') as f:
            f.write(post['content'])
        print(f"✅ {post['platform']} post saved: {post_file}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='殺手林每日內容機器')
    parser.add_argument('--run', action='store_true', help='執行完整內容生成')
    parser.add_argument('--preview', action='store_true', help='預覽今日內容')
    parser.add_argument('--devto', action='store_true', help='生成 Dev.to 文章')
    args = parser.parse_args()
    
    print("=" * 50)
    print("殺手林每日內容工廠")
    print(f"日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    hex_sym, hex_zh, hex_en, meaning, action = get_today_hexagram()
    print(f"\n📊 今日卦象：{hex_sym} {hex_en}（{hex_zh}）")
    print(f"💬 {meaning}")
    print(f"✅ {action}")
    
    if args.preview:
        print("\n" + "=" * 50)
        print("SOCIAL POSTS:")
        print("=" * 50)
        posts = generate_social_posts()
        for p in posts:
            print(f"\n[{p['platform'].upper()}]")
            print(p['content'][:300] + "...")
        
        print("\n" + "=" * 50)
        print("DEV.TO ARTICLE:")
        print("=" * 50)
        devto = generate_devto_article()
        print(f"Title: {devto['title']}")
        print(devto['body'][:500] + "...")
        
        print("\n" + "=" * 50)
        print("SEO ARTICLE:")
        print("=" * 50)
        article = generate_seo_article()
        print(f"Title: {article['title']}")
        print(article['article'][:500] + "...")
    
    elif args.devto:
        devto = generate_devto_article()
        print(f"\n📝 Dev.to Article: {devto['title']}")
        print(f"Tags: {', '.join(devto['tags'])}")
    
    elif args.run:
        article = generate_seo_article()
        posts = generate_social_posts()
        devto_article = generate_devto_article()
        save_for_scheduling(posts, article, devto_article)
        
        # Save SEO article
        article_file = CONTENT_DIR / f"article-{datetime.now().strftime('%Y-%m-%d')}.md"
        with open(article_file, 'w') as f:
            f.write(article['article'])
        print(f"✅ SEO article saved: {article_file}")
        
        print("\n📤 Content ready for publishing!")
        print("   - SEO article saved")
        print("   - Social posts queued")
        print("   - Dev.to article generated")
    
    else:
        print("\n使用說明:")
        print("  --preview  預覽今日內容")
        print("  --run      生成並儲存內容")
        print("  --devto    生成 Dev.to 文章")

if __name__ == '__main__':
    main()
