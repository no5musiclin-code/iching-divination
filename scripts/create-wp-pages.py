#!/usr/bin/env python3
"""
殺手林 WordPress 頁面批量建立腳本
使用 WordPress.com XML-RPC API 建立頁面
"""
import xmlrpc.client
import re

# WordPress.com 設定
WORDPRESS_URL = "https://shaishalin.wordpress.com/xmlrpc.php"
USERNAME = "linblance@gmail.com"
APP_PASSWORD = "chwe wvdk oeyy wuzx"  # WordPress.com application password

# AI 工具中心母頁面 ID
PARENT_PAGE_ID = 29  # 從剛才建立的頁面而來

def create_page(title, content, parent_id=0, slug=""):
    """建立 WordPress 頁面"""
    try:
        server = xmlrpc.client.ServerProxy(WORDPRESS_URL)
        result = server.wp.newPost(
            0,  # blog_id，WordPress.com 永遠是 0
            USERNAME,
            APP_PASSWORD,
            {
                'post_type': 'page',
                'post_title': title,
                'post_content': content,
                'post_status': 'publish',
                'post_name': slug,
                'post_parent': parent_id,
            }
        )
        return result
    except Exception as e:
        return f"ERROR: {e}"

# 頁面內容定義
PAGES = [
    {
        'title': '易經測字問事｜線上免費卜卦',
        'content': '''<h2>🔮 易經測字問事</h2>
<p>輸入你的問題，讓 AI 根據易經象數為你解讀。涵蓋投資、感情、事業等人生各大課題，完全免費使用。</p>
<h3>📖 如何使用</h3>
<ol>
<li>在下方輸入你想問的問題（如：我的事業運勢如何？）</li>
<li>真誠地想著你的問題，心中默念 3 秒</li>
<li>點擊「開始卜卦」取得你的易經卦象</li>
</ol>
<h3>💡 這個工具適合誰？</h3>
<ul>
<li>🤔 遇到重大決定，不知如何選擇</li>
<li>💼 想了解事業或創業的運勢</li>
<li>💕 想透視感情關係的走向</li>
<li>💰 想評估投資或財務決策</li>
</ul>
<h3>⚠️ 免費工具說明</h3>
<p>這是一個實驗性工具，結合易經象數與 AI 邏輯分析，提供參考性的建議。建議僅供參考，不作為重大決策的唯一依據。</p>
<p style="text-align:center; margin-top:2rem;"><a href="https://shaishalin.wordpress.com/iching" style="background:#d4af37; color:#0a0a0f; padding:1rem 2rem; border-radius:30px; font-weight:bold; text-decoration:none; display:inline-block;">🚀 立即使用易經測字</a></p>''',
        'slug': 'iching',
        'parent': PARENT_PAGE_ID,
    },
    {
        'title': '投資複利計算機｜免費線上工具',
        'content': '''<h2>📊 投資複利計算機</h2>
<p>計算你的長期投資成果，看看時間 + 複利的力量有多大！完全免費使用。</p>
<h3>📈 功能特色</h3>
<ul>
<li>💰 支援定期定額與一次投入</li>
<li>📅 可設定投資期限（1-40年）</li>
<li>📊 即時顯示本利和曲線圖</li>
<li>🌱 展示時間複利的神奇效果</li>
</ul>
<h3>🎯 為什麼要用這個工具？</h3>
<p>很多人低估了時間在投資中的力量。這個計算機讓你一目了然地看到：</p>
<ul>
<li>每月存 $5,000，20 年後是多少？</li>
<li>不同的年化報酬率對最終結果的影響？</li>
<li>提早投資 5 年與晚了 5 年的差別？</li>
</ul>
<p style="text-align:center; margin-top:2rem;"><a href="https://shaishalin.wordpress.com/calculator" style="background:#22c55e; color:#fff; padding:1rem 2rem; border-radius:30px; font-weight:bold; text-decoration:none; display:inline-block;">🚀 立即計算你的複利</a></p>''',
        'slug': 'calculator',
        'parent': PARENT_PAGE_ID,
    },
    {
        'title': 'SEO 關鍵字探索器｜免費關鍵字分析工具',
        'content': '''<h2>🔍 SEO 關鍵字探索器</h2>
<p>10 分鐘完成文章架構，找出最有價值的關鍵字策略。內容創作者必備工具！</p>
<h3>🎯 功能特色</h3>
<ul>
<li>📊 搜尋量估算</li>
<li>🎯 關鍵字難度分析</li>
<li>📝 相關關鍵字建議</li>
<li>📋 一鍵匯出文章大綱</li>
</ul>
<h3>💡 適用場景</h3>
<ul>
<li>📰 寫部落格文章前的關鍵字研究</li>
<li>🏪 WooCommerce 商品關鍵字優化</li>
<li>📱 內容行銷策略規劃</li>
<li>🌍 多語言市場關鍵字探索</li>
</ul>
<p style="text-align:center; margin-top:2rem;"><a href="https://shaishalin.wordpress.com/keyword" style="background:#3b82f6; color:#fff; padding:1rem 2rem; border-radius:30px; font-weight:bold; text-decoration:none; display:inline-block;">🚀 開始關鍵字研究</a></p>''',
        'slug': 'keyword',
        'parent': PARENT_PAGE_ID,
    },
    {
        'title': '創業者性格測驗｜了解你的天賦與盲點',
        'content': '''<h2>🎯 創業者性格測驗</h2>
<p>了解你是哪種類型的創業家，找出你的天賦與需要克服的盲點。免費、5 分鐘完成！</p>
<h3>🔬 測驗內容</h3>
<ul>
<li>🎨 你的創業人格類型</li>
<li>⚡ 先天優勢與劣勢分析</li>
<li>💼 適合的商業模式</li>
<li>📊 失敗風險與防範</li>
</ul>
<h3>💡 這個測驗適合誰？</h3>
<ul>
<li>🤔 想創業但不知道適合什麼方向</li>
<li>🚀 已經在創業想知道如何提升</li>
<li>💡 想了解合作夥伴的創業特質</li>
</ul>
<p style="text-align:center; margin-top:2rem;"><a href="https://shaishalin.wordpress.com/quiz" style="background:#8b5cf6; color:#fff; padding:1rem 2rem; border-radius:30px; font-weight:bold; text-decoration:none; display:inline-block;">🚀 開始測驗</a></p>''',
        'slug': 'quiz',
        'parent': PARENT_PAGE_ID,
    },
    {
        'title': '每日星座運勢｜12星座完整運勢查詢',
        'content': '''<h2>✨ 每日星座運勢</h2>
<p>每天更新 12 星座完整運勢，涵蓋愛情、事業、財運三大領域！</p>
<h3>🌟 功能特色</h3>
<ul>
<li>♈ 12 星座完整覆蓋</li>
<li>📅 每日更新</li>
<li>💕 愛情運勢分析</li>
<li>💼 事業/學業運勢</li>
<li>💰 財運指數</li>
</ul>
<h3>🎯 使用方式</h3>
<p>選擇你的星座，立即取得今日完整運勢預測！</p>
<p style="text-align:center; margin-top:2rem;"><a href="https://shaishalin.wordpress.com/horoscope" style="background:#ec4899; color:#fff; padding:1rem 2rem; border-radius:30px; font-weight:bold; text-decoration:none; display:inline-block;">🚀 查看我的星座運勢</a></p>''',
        'slug': 'horoscope',
        'parent': PARENT_PAGE_ID,
    },
    {
        'title': '抽獎轉盤工具｜活動必備線上工具',
        'content': '''<h2>🎰 免費抽獎轉盤工具</h2>
<p>舉辦活動必備！可自訂獎品內容，公平公開的線上抽獎工具。</p>
<h3>🎯 功能特色</h3>
<ul>
<li>⚙️ 完全自訂獎品名稱與數量</li>
<li>🎲 公平隨機抽出</li>
<li>📱 手機電腦都能用</li>
<li>🔗 一鍵分享轉盤連結</li>
</ul>
<h3>💡 適用場景</h3>
<ul>
<li>🎉 公司年會抽獎</li>
<li>📱 社群媒體活動</li>
<li>🏫 學校或社團活動</li>
<li>🛒 電商促銷活動</li>
</ul>
<p style="text-align:center; margin-top:2rem;"><a href="https://shaishalin.wordpress.com/spinwheel" style="background:#f59e0b; color:#fff; padding:1rem 2rem; border-radius:30px; font-weight:bold; text-decoration:none; display:inline-block;">🚀 立即使用抽獎轉盤</a></p>''',
        'slug': 'spinwheel',
        'parent': PARENT_PAGE_ID,
    },
]

def main():
    print("=== 殺手林 WordPress 頁面批量建立 ===\n")
    
    for i, page in enumerate(PAGES):
        print(f"[{i+1}/{len(PAGES)}] 建立頁面: {page['title']}")
        result = create_page(
            title=page['title'],
            content=page['content'],
            parent_id=page.get('parent', 0),
            slug=page.get('slug', '')
        )
        if isinstance(result, str) and result.startswith("ERROR"):
            print(f"  ❌ 失敗: {result}")
        else:
            print(f"  ✅ 完成！頁面 ID: {result}")
        print()

if __name__ == "__main__":
    main()
