#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
殺手林 WordPress 每日自動發文系統
每日根據易經卦象自動生成並發布 SEO 文章
"""

import json
import random
import datetime
import time
import sys
import os
import re

# 易經八卦基本資料
HEXAGRAMS = [
    {"name": "乾為天", "symbol": "䷀", "meaning": "創造、力量、領導", "career": "大胆决策、勇於開創", "wealth": "投資擴張、正財運強"},
    {"name": "坤為地", "symbol": "䷁", "meaning": "順從、包容、穩健", "career": "穩健經營、團隊合作", "wealth": "積少成多、保守理財"},
    {"name": "水雷屯", "symbol": "䷂", "meaning": "萌芽、困難、積累", "career": "初期建設、耐心布局", "wealth": "播種期、小額投入"},
    {"name": "山水蒙", "symbol": "䷃", "meaning": "啟蒙、迷惘、求知", "career": "學習充電、尋求指導", "wealth": "教育投資、知識付費"},
    {"name": "水天需", "symbol": "䷄", "meaning": "等待、耐心、期望", "career": "等待時機、儲備能量", "wealth": "耐心等待、審慎理財"},
    {"name": "天水讼", "symbol": "䷅", "meaning": "爭論、訴訟、衝突", "career": "協商調解、避免對抗", "wealth": "保守理財、遠離紛爭"},
    {"name": "地水師", "symbol": "䷆", "meaning": "統帥、領導、紀律", "career": "領導團隊、建立制度", "wealth": "團隊收益、統一理財"},
    {"name": "水地比", "symbol": "䷇", "meaning": "親密、合作、和諧", "career": "建立合作關係", "wealth": "合作共贏、分享財富"},
    {"name": "風天小畜", "symbol": "䷐", "meaning": "積蓄、準備、初成", "career": "积累资源、蓄势待发", "wealth": "小額積蓄、穩步增長"},
    {"name": "天澤履", "symbol": "䷑", "meaning": "謹慎、履行、順序", "career": "按部就班、謹守原則", "wealth": "腳踏實地、正當收入"},
    {"name": "地天泰", "symbol": "䷊", "meaning": "通泰、祥和、上下交流", "career": "萬事亨通、推廣合作", "wealth": "財運亨通、貴人相助"},
    {"name": "天地否", "symbol": "䷋", "meaning": "閉塞、對立、不通", "career": "保守經營、收縮調整", "wealth": "守成為宜、控制支出"},
    {"name": "天火同人", "symbol": "䷌", "meaning": "同儕、和合、廣泛合作", "career": "擴展人脈、團隊整合", "wealth": "合夥投資、共分收益"},
    {"name": "火天大有", "symbol": "䷍", "meaning": "豐收、富有、包容", "career": "事業高峰、收獲季節", "wealth": "財富大增、回饋社會"},
    {"name": "地山謙", "symbol": "䷎", "meaning": "謙遜、低下、內斂", "career": "低調行事、累積實力", "wealth": "穩健積累、不露財富"},
    {"name": "雷地豫", "symbol": "䷏", "meaning": "喜悅、預備、娛樂", "career": "準備充分、把握機會", "wealth": "娱樂休閒、創意收入"},
    {"name": "澤雷隨", "symbol": "䷐", "meaning": "隨從、彈性、順應", "career": "靈活應變、抓住潮流", "wealth": "跟隨趨勢、順勢而為"},
    {"name": "風地觀", "symbol": "䷓", "meaning": "觀察、借鑒、榜樣", "career": "觀察市場、學習標竿", "wealth": "觀望期、參考他人"},
    {"name": "火雷噬嗑", "symbol": "䷔", "meaning": "咬合、決斷、執行", "career": "果斷執行、掃除障礙", "wealth": "強力執行、突破難關"},
    {"name": "山火賁", "symbol": "䷕", "meaning": "裝飾、文飾、美化", "career": "品牌形象、包裝行銷", "wealth": "包装價值、提升價格"},
    {"name": "山地剝", "symbol": "䷖", "meaning": "剝落、消耗、蕭條", "career": "收縮戰線、保存實力", "wealth": "節流為主、避免擴張"},
    {"name": "地雷復", "symbol": "䷗", "meaning": "恢復、回歸、新生", "career": "重新出發、修復關係", "wealth": "反彈回升、重新佈局"},
    {"name": "天雷无妄", "symbol": "䷘", "meaning": "無妄、不虛偽、自然", "career": "真誠行事、避免投機", "wealth": "正當途徑、誠信致富"},
    {"name": "山天大畜", "symbol": "䷙", "meaning": "大積蓄、潛力、等待", "career": "大量積累、培養人才", "wealth": "長期投資、厚積薄發"},
    {"name": "山澤損", "symbol": "䷚", "meaning": "減少、節制、犧牲", "career": "降低成本、精簡人員", "wealth": "節省開支、斷尾求生"},
    {"name": "風雷益", "symbol": "䷛", "meaning": "利益、增益、增加", "career": "擴大規模、增加收益", "wealth": "投資獲利、資產增值"},
    {"name": "澤天夬", "symbol": "䷜", "meaning": "決定、決裂、果斷", "career": "快速決策、清除小人", "wealth": "決策果斷、把握良機"},
    {"name": "天風姤", "symbol": "䷝", "meaning": "邂逅、機會、監控", "career": "抓住機會、廣結人脈", "wealth": "把握機遇、多元發展"},
    {"name": "澤地萃", "symbol": "䷞", "meaning": "聚集、薈萃、精華", "career": "人才聚集、資源整合", "wealth": "集合資源、共享財富"},
    {"name": "地風昇", "symbol": "䷟", "meaning": "上升、升進、發展", "career": "步步高升、職位晉升", "wealth": "穩步增長、持續獲利"},
    {"name": "澤水困", "symbol": "䷱", "meaning": "困境、艱難、忍耐", "career": "堅守崗位、耐心等待", "wealth": "艱困時期、保守理財"},
    {"name": "水風井", "symbol": "䷲", "meaning": "井泉、恒常、修養", "career": "建立系統、培養習慣", "wealth": "穩定收入、源源不絕"},
    {"name": "澤火革", "symbol": "䷯", "meaning": "改革、變革、創新", "career": "大膽改革、破舊立新", "wealth": "變革帶財、突破框架"},
    {"name": "火風鼎", "symbol": "䷱", "meaning": "鼎立、穩定、權威", "career": "建立制度、樹立標準", "wealth": "確立地位、穩定收益"},
    {"name": "震為雷", "symbol": "䷲", "meaning": "震動、警覺、驚醒", "career": "把握機會、快速行動", "wealth": "危機入市、膽大心細"},
    {"name": "艮為山", "symbol": "䷳", "meaning": "停止、節制、靜止", "career": "適時停止、審視全局", "wealth": "暫停投資、觀望局勢"},
    {"name": "風山漸", "symbol": "䷴", "meaning": "漸進、順序、耐心", "career": "循序漸進、按序進行", "wealth": "分期投資、穩步致富"},
    {"name": "雷澤歸妹", "symbol": "䷵", "meaning": "歸宿、婚嫁、合作", "career": "歸屬合作、找到定位", "wealth": "合作共贏、穩定收入"},
    {"name": "雷火豐", "symbol": "䷶", "meaning": "豐盛、盛大、豐收", "career": "事業高峰、擴大經營", "wealth": "財富高峰、多元收入"},
    {"name": "火山旅", "symbol": "䷷", "meaning": "旅行、流浪、不穩", "career": "外出發展、探索新市場", "wealth": "奔波求財、不宜守成"},
    {"name": "巽為風", "symbol": "䷸", "meaning": "風、滲透、柔和", "career": "渗透市場、低調擴張", "wealth": "隱性收入、間接獲利"},
    {"name": "兌為澤", "symbol": "䷹", "meaning": "喜悅、湖泊、交流", "career": "溝通協調、公關外交", "wealth": "口才獲利、服務收入"},
    {"name": "風澤中孚", "symbol": "䷼", "meaning": "誠信、信任、忠實", "career": "建立信任、品牌誠信", "wealth": "誠信經商、長期收益"},
    {"name": "雷山小過", "symbol": "䷽", "meaning": "小過、跨越、補救", "career": "小步快跑、及時修正", "wealth": "小額投資、及時止損"},
    {"name": "水火既濟", "symbol": "䷾", "meaning": "完成、陰陽平衡", "career": "事業完成、進入新階段", "wealth": "功德圓满、穩定收益"},
    {"name": "火水未濟", "symbol": "䷿", "meaning": "未完成、陰陽失衡", "career": "重新調整、尋找平衡", "wealth": "重整旗鼓、重新開始"},
]

INDUSTRIES = [
    "AI工具", "電商", "內容創作", "聯盟行銷", "SaaS", "自媒體",
    "線上課程", "數位產品", "跨境電商", "自由接案", "區塊鏈", "網路行銷"
]

AFFILIATE_LINKS = {
    "AI工具": "https://shaishalin.wordpress.com/ai-tools-recommendation/",
    "線上課程": "https://shaishalin.wordpress.com/online-courses/",
    "電子書": "https://shaishalin.wordpress.com/ebooks/",
    "創業工具": "https://shaishalin.wordpress.com/startup-tools/",
    "默认": "https://shaishalin.wordpress.com/recommended-tools/"
}


def load_topics():
    """載入文章主題庫"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    topics_path = os.path.join(script_dir, "daily-topics.json")
    with open(topics_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_config():
    """載入設定檔"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "wp-config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_config(config):
    """儲存設定檔"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "wp-config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_day_hexagram():
    """根據日期取得當日卦象（每天固定一個卦）"""
    today = datetime.date.today()
    # 用日期計算確保同一天同一卦象
    seed = today.year * 10000 + today.month * 100 + today.day
    random.seed(seed)
    index = random.randint(0, len(HEXAGRAMS) - 1)
    random.seed()  # 重置隨機種子
    return HEXAGRAMS[index]


def get_day_topic():
    """根據日期選擇當日主題"""
    today = datetime.date.today()
    topics = load_topics()
    # 用日期計算確保同一天同一主題
    seed = today.year * 10000 + today.month * 100 + today.day + today.timetuple().tm_yday
    random.seed(seed)
    topic = random.choice(topics)
    random.seed()  # 重置
    return topic


def get_industry():
    """根據日期選擇當日產業"""
    today = datetime.date.today()
    seed = today.year * 10000 + today.month * 100 + today.day + 7
    random.seed(seed)
    industry = random.choice(INDUSTRIES)
    random.seed()
    return industry


def generate_article_content(hexagram, topic, industry):
    """生成 SEO 文章內容（HTML格式）"""
    
    # 隨機選擇三個行動呼籲
    actions = [
        f"1️⃣ 立即行動：今天就開始應用{hexagram['name']}的智慧到你的{industry}事業中",
        f"2️⃣ 深度學習：閱讀更多關於{hexagram['name']}在{industry}領域的應用案例",
        f"3️⃣ 付費內容：點擊了解殺手林針對{industry}創業者的完整策略方案"
    ]
    random.seed()
    random.shuffle(actions)
    actions_text = "\n".join(actions[:3])
    
    # 取得相關聯盟連結
    affiliate_link = AFFILIATE_LINKS.get(industry, AFFILIATE_LINKS["默认"])
    
    # 取得日期用於顯示
    today = datetime.date.today()
    date_str = today.strftime("%Y年%m月%d日")
    
    content = f"""
<h2>📅 {date_str} 每日創業能量預測</h2>

<p>各位創業者朋友，今天是<strong>{date_str}</strong>。殺手林每天都會根據易經為你解讀今日的創業運勢，幫助你在正確的時間做正確的決定。</p>

<h2>🔮 今日卦象：{hexagram['name']} {hexagram['symbol']}</h2>

<p>今日為你帶來的卦象是<strong>{hexagram['name']}</strong>——</p>

<blockquote>
<p><em>{hexagram['meaning']}</em></p>
</blockquote>

<p>這個卦象象徵著：{hexagram['name']}代表的是一種特定的人生狀態和宇宙規律。讓我們一起看看它在今日的創業領域裡，能給你什麼樣的啟示。</p>

<h2>💼 事業啟示</h2>

<p>根據{hexagram['name']}的能量，今日在事業方面：</p>

<ul>
<li><strong>核心主題：</strong>{hexagram['career']}</li>
<li><strong>貴人方位：</strong>東北方或西南方</li>
<li><strong>注意事情：</strong>避免過度保守或過度冒進</li>
<li><strong>幸運數字：</strong>{random.randint(1,9)}, {random.randint(10,99)}</li>
</ul>

<h2>💰 財富能量</h2>

<p>在財務層面，{hexagram['name']}帶來的指引是：</p>

<ul>
<li><strong>財運特質：</strong>{hexagram['wealth']}</li>
<li><strong>適合時機：</strong>上午9-11點，下午3-5點</li>
<li><strong>避開時段：</strong>清晨5-7點</li>
<li><strong>幸運色：</strong>{random.choice(['紅色', '金色', '藍色', '綠色', '紫色', '白色'])}</li>
</ul>

<h2>🎯 {industry}創業者今日重點</h2>

<p>如果你正在從事<strong>{industry}</strong>相關的創業項目，{hexagram['name']}給你以下具體建議：</p>

<ol>
<li><strong>認知調整：</strong>今天的能量適合重新審視你的{industry}事業策略，問問自己：現有的方向是否與市場趨勢一致？</li>
<li><strong>行動重點：</strong>{hexagram['career']}——這是你今天最應該投入的方向</li>
<li><strong>風險提示：</strong>在{industry}領域，今日需要注意{random.choice(['現金流管理', '團隊溝通', '客戶關係', '產品品質', '市場推廣'])}的環節</li>
</ol>

<h2>🚀 今日三個具體行動</h2>

<p>根據易經{hexagram['name']}的指引，殺手林建議你今天執行以下三個行動：</p>

<p>{actions_text}</p>

<h2>📚 易經小知識：什麼是{hexagram['name']}？</h2>

<p>{hexagram['name']}是易經六十四卦之一，由{random.randint(3,8)}個陽爻和{random.randint(3,8)}個陰爻組成。在古代，這個卦象通常預示著{random.choice(['機遇與挑戰並存', '需要耐心等待', '適合大膽行動', '適合收斂整理', '適合總結規劃'])}的時期。</p>

<p>對於現代創業者來說，易經的智慧可以幫助你：</p>
<ul>
<li>在正確的時機做正確的決定</li>
<li>理解市場週期和創業節奏</li>
<li>在逆境中保持平靜和專注</li>
</ul>

<h2>💡 殺手林說</h2>

<p>創業這條路，技術能力只佔30%，剩下的70%是認知、決策和執行。而易經，正是幫助你提升認知層次的古老智慧。</p>

<p>每天跟著殺手林用易經算一算，讓古老的智慧為你的現代創業護航！</p>

<hr/>

<p><strong>🔗 相關資源：</strong></p>
<ul>
<li><a href="{AFFILIATE_LINKS['AI工具']}" target="_blank">AI工具推薦清單</a></li>
<li><a href="{AFFILIATE_LINKS['創業工具']}" target="_blank">創業必備工具</a></li>
<li><a href="{AFFILIATE_LINKS['線上課程']}" target="_blank">殺手林線上課程</a></li>
</ul>

<p><em>🔔 記得追蹤「殺手林」獲取每日創業易經預測！</em></p>
"""
    
    return content.strip()


def generate_seo_title(hexagram, topic, industry):
    """生成 SEO 標題"""
    title = topic["title"]
    title = title.replace("{hexagram}", hexagram["name"])
    title = title.replace("{industry}", industry)
    return title


def generate_excerpt(hexagram, industry):
    """生成文章摘要"""
    return f"今日易經創業預測｜{hexagram['name']}為你解讀{industry}事業的機會與挑戰，涵蓋財運、事業、感情三大方向的實用建議。"


def test_xmlrpc_connection(site_url, username, app_password):
    """測試 XML-RPC 連線"""
    import xmlrpc.client
    
    try:
        rpc_url = site_url.rstrip("/") + "/xmlrpc.php"
        server = xmlrpc.client.ServerProxy(rpc_url)
        
        # 測試：用 system.listMethods 查看可用方法
        methods = server.system.listMethods()
        
        return {
            "success": True,
            "rpc_url": rpc_url,
            "methods": len(methods),
            "message": "XML-RPC 連線成功"
        }
    except xmlrpc.client.Fault as e:
        return {
            "success": False,
            "error": f"XML-RPC 錯誤: {e.faultString}",
            "message": "認證或權限問題"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "無法連線到 WordPress"
        }


def publish_to_wordpress(title, content, excerpt, categories, tags, site_url, username, app_password, scheduled_date=None):
    """發布文章到 WordPress"""
    import xmlrpc.client
    
    try:
        rpc_url = site_url.rstrip("/") + "/xmlrpc.php"
        server = xmlrpc.client.ServerProxy(rpc_url)
        
        # 文章內容
        post = {
            "post_type": "post",
            "post_status": "publish",
            "post_title": title,
            "post_content": content,
            "post_excerpt": excerpt,
            "terms_names": {
                "category": categories,
                "post_tag": tags
            }
        }
        
        # 如果有排程時間
        if scheduled_date:
            post["post_date"] = scheduled_date.strftime("%Y-%m-%d %H:%M:%S")
            post["post_status"] = "future"
        
        # 發布
        result = server.wp.newPost(0, username, app_password, post)
        
        return {
            "success": True,
            "post_id": result,
            "url": f"{site_url}/?p={result}",
            "message": "文章發布成功"
        }
        
    except xmlrpc.client.Fault as e:
        return {
            "success": False,
            "error": f"XML-RPC 錯誤: {e.faultString}",
            "message": "發布失敗"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "發布時發生錯誤"
        }


def setup_auth_interactive():
    """互動式設定認證資訊"""
    print("\n" + "="*50)
    print("🔐 WordPress 認證設定")
    print("="*50)
    print("\n請前往 WordPress.com 產生應用程式密碼：")
    print("1. 登入 https://wordpress.com")
    print("2. 前往 https://wordpress.com/me/security")
    print("3. 點擊「應用程式密碼」")
    print("4. 輸入名稱（如：daily-post-bot」）")
    print("5. 複製產生的密碼")
    print("")
    
    site_url = input("WordPress 網址 [https://shaishalin.wordpress.com]: ").strip()
    if not site_url:
        site_url = "https://shaishalin.wordpress.com"
    
    username = input("使用者名稱或 Email [linblance@gmail.com]: ").strip()
    if not username:
        username = "linblance@gmail.com"
    
    app_password = input("應用程式密碼: ").strip()
    
    return {
        "site_url": site_url,
        "username": username,
        "app_password": app_password
    }


def main():
    print("\n" + "="*60)
    print("🔮 殺手林 WordPress 每日自動發文系統")
    print("="*60 + "\n")
    
    # 取得今日卦象和主題
    hexagram = get_day_hexagram()
    topic = get_day_topic()
    industry = get_industry()
    
    print(f"📅 今日日期：{datetime.date.today().strftime('%Y年%m月%d日')}")
    print(f"🔮 今日卦象：{hexagram['name']} {hexagram['symbol']}")
    print(f"📝 今日主題：{topic['title'].replace('{hexagram}', hexagram['name']).replace('{industry}', industry)}")
    print(f"🏭 針對產業：{industry}")
    print()
    
    # 載入或設定認證
    config = load_config()
    
    if not config:
        print("⚠️ 尚未設定 WordPress 認證資訊")
        config = setup_auth_interactive()
        save_config(config)
        print("✅ 設定已儲存")
    
    # 測試模式（不傳參數時）
    if len(sys.argv) == 1:
        mode = "test"
    elif len(sys.argv) >= 2 and sys.argv[1] == "--publish":
        mode = "publish"
    elif len(sys.argv) >= 2 and sys.argv[1] == "--setup":
        config = setup_auth_interactive()
        save_config(config)
        print("✅ 設定已更新")
        return
    else:
        mode = "test"
    
    # 測試連線
    print("\n🔌 測試 WordPress XML-RPC 連線...")
    test_result = test_xmlrpc_connection(
        config["site_url"],
        config["username"],
        config["app_password"]
    )
    
    if test_result["success"]:
        print(f"✅ {test_result['message']}")
        print(f"   URL: {test_result['rpc_url']}")
    else:
        print(f"❌ 連線失敗：{test_result['message']}")
        print(f"   錯誤：{test_result.get('error', '未知錯誤')}")
        print("\n💡 解決方案：")
        print("1. 確認應用程式密碼正確")
        print("2. 確認 WordPress.com 帳戶已啟用 XML-RPC")
        print("3. 或使用 --setup 重新設定")
        
        # 嘗試瀏覽器方式（browser method）
        print("\n🔄 嘗試瀏覽器自動化方式發布...")
        return {
            "success": False,
            "mode": "browser_required",
            "message": "需要瀏覽器方式發布"
        }
    
    # 生成文章
    print("\n✍️ 生成文章內容...")
    title = generate_seo_title(hexagram, topic, industry)
    content = generate_article_content(hexagram, topic, industry)
    excerpt = generate_excerpt(hexagram, industry)
    
    print(f"   標題：{title}")
    print(f"   字數：約 {len(content)} 字")
    
    # 設定分類和標籤
    categories = ["創業", "易經", "AI工具"]
    tags = ["易經創業", hexagram["name"], industry, "每日預測", "殺手林"]
    
    if mode == "test":
        print("\n📋 測試模式：文章已生成，但尚未發布")
        print("   若要發布，請使用：python3 daily-wordpress-post.py --publish")
        return {
            "success": True,
            "mode": "test",
            "title": title,
            "excerpt": excerpt,
            "word_count": len(content),
            "hexagram": hexagram,
            "industry": industry,
            "message": "測試模式完成"
        }
    
    # 發布文章
    print("\n🚀 發布文章到 WordPress...")
    
    # 計算明天早上 8:00 為排程時間
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    scheduled = datetime.datetime.combine(tomorrow, datetime.time(8, 0, 0))
    # 轉換為 WordPress 使用的 UTC 時間（台灣是 UTC+8，所以減8小時）
    scheduled_utc = scheduled - datetime.timedelta(hours=8)
    
    result = publish_to_wordpress(
        title=title,
        content=content,
        excerpt=excerpt,
        categories=categories,
        tags=tags,
        site_url=config["site_url"],
        username=config["username"],
        app_password=config["app_password"],
        scheduled_date=None  # 立即發布；若要排程，改用 scheduled_utc
    )
    
    if result["success"]:
        print(f"✅ 文章發布成功！")
        print(f"   標題：{result.get('title', title)}")
        print(f"   URL：{result.get('url', '#')}")
        print(f"   文章ID：{result.get('post_id', 'N/A')}")
    else:
        print(f"❌ 發布失敗：{result['message']}")
        if "error" in result:
            print(f"   錯誤：{result['error']}")
    
    return result


if __name__ == "__main__":
    result = main()
    
    # 顯示結果摘要
    print("\n" + "="*60)
    print("📊 執行結果摘要")
    print("="*60)
    if isinstance(result, dict):
        print(f"成功與否：{'✅ 成功' if result.get('success') else '❌ 失敗'}")
        print(f"模式：{result.get('mode', 'N/A')}")
        if result.get('title'):
            print(f"文章標題：{result.get('title')}")
        if result.get('url'):
            print(f"文章網址：{result.get('url')}")
        if result.get('message'):
            print(f"訊息：{result.get('message')}")
    print()
