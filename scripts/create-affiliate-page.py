#!/usr/bin/env python3
"""建立推薦工具箱 WordPress 頁面"""
import urllib.request
import urllib.parse
import json
import re
import http.cookiejar

# WordPress 登入資訊
WP_URL = "https://shaishalin.wordpress.com"
LOGIN_URL = f"{WP_URL}/wp-login.php"
REST_URL = f"{WP_URL}/wp-json/wp/v2/pages"

# 讀取 nonce
def get_nonce(cookies):
    req = urllib.request.Request(
        "https://shaishalin.wordpress.com/wp-admin/post-new.php?post_type=page",
        headers={"Cookie": cookies}
    )
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode()
    m = re.search(r'wp-api-nonce" content="([^"]+)"', html)
    if m:
        return m.group(1)
    m = re.search(r'nonce:\s*["\']([^"\']+)["\']', html)
    if m:
        return m.group(1)
    return None

# 讀取 cookies
def load_cookies():
    jar = http.cookiejar.MozillaCookieJar('/tmp/wp_cookies.txt')
    try:
        jar.load(ignore_discard=True)
        cookies = "; ".join(f"{c.name}={c.value}" for c in jar)
        return cookies, jar
    except:
        return None, None

cookies, jar = load_cookies()
if not cookies:
    print("❌ 無法讀取 cookies")
    exit(1)

nonce = get_nonce(cookies)
print(f"Nonce: {nonce}")

# 頁面內容
title = "殺手林推薦工具箱｜AI創業必備工具清單"
content = """<h2>🤖 AI 創業推薦工具</h2>
<p>這些工具是殺手林在建立線上事業過程中實際使用並驗證有效的工具。每個工具旁邊的連結是聯盟連結，如果你透過這些連結購買，我可能會獲得一小筆佣金，但不會增加你的費用。這是支持殺手林持續創作的最佳方式之一 🙏</p>

<h3>📧 Email 行銷工具</h3>
<ul>
<li><strong>Kit（ConvertKit）</strong> — 最適合內容創作者的 Email 行銷平台，幫你建立清單、自動化發送、銷售數位商品。<br><a href="https://kit.com/" target="_blank" rel="noopener">查看 Kit →</a>（聯盟連結待更新）</li>
<li><strong>Mailchimp</strong> — 免費開始，適合新手的 Email 行銷工具。<br><a href="https://mailchimp.com/" target="_blank" rel="noopener">查看 Mailchimp →</a></li>
</ul>

<h3>🛠️ 網站與托管</h3>
<ul>
<li><strong>WordPress.com</strong> — 建立部落格和網站的首選平台。<br><a href="https://wordpress.com/" target="_blank" rel="noopener">查看 WordPress.com →</a></li>
<li><strong>Cloudflare</strong> — 免費 CDN 和安全性保護。<br><a href="https://cloudflare.com/" target="_blank" rel="noopener">查看 Cloudflare →</a></li>
</ul>

<h3>✍️ 內容創作 AI 工具</h3>
<ul>
<li><strong>Claude</strong> — 最強大的 AI 寫作助理，適合內容創作和商業策略。<br><a href="https://claude.ai/" target="_blank" rel="noopener">查看 Claude →</a></li>
<li><strong>ChatGPT</strong> — OpenAI 的 AI 助手，適合各種任務。<br><a href="https://chatgpt.com/" target="_blank" rel="noopener">查看 ChatGPT →</a></li>
<li><strong>Canva</strong> — 無需設計技能，AI 幫你做圖。<br><a href="https://canva.com/" target="_blank" rel="noopener">查看 Canva →</a></li>
</ul>

<h3>💰 聯盟行銷與變現</h3>
<ul>
<li><strong>Amazon Associates</strong> — 全球最大的聯盟行銷平台。<br><a href="https://affiliate-program.amazon.com/" target="_blank" rel="noopener">查看 Amazon Associates →</a></li>
<li><strong>Ko-fi</strong> — 免費建立商店，接受贊助和銷售數位商品。<br><a href="https://ko-fi.com/shaishalin" target="_blank" rel="noopener">查看 Ko-fi →</a></li>
</ul>

<h3>📊 SEO 與關鍵字研究</h3>
<ul>
<li><strong>Google Analytics</strong> — 免費流量分析工具。<br><a href="https://analytics.google.com/" target="_blank" rel="noopener">查看 Google Analytics →</a></li>
</ul>

<h3>💡 創業工具</h3>
<ul>
<li><strong>Notion</strong> — 萬用的生產力工具，組織你的創業任務。<br><a href="https://notion.so/" target="_blank" rel="noopener">查看 Notion →</a></li>
<li><strong>Google Workspace</strong> — Gmail、Google Drive、Google Doc 創業必備。<br><a href="https://workspace.google.com/" target="_blank" rel="noopener">查看 Google Workspace →</a></li>
</ul>

<hr>

<p style="background:rgba(167,139,250,0.1);padding:1rem 1.25rem;border-radius:12px;text-align:center;">
<strong>💼 想要系統化學習創業技能？</strong><br>
<a href="https://ko-fi.com/s/00367ecd74" style="color:#a78bfa;">查看殺手林 AI 創業工具包 →</a>
</p>
"""

# 建立頁面
data = json.dumps({
    "title": title,
    "content": content,
    "status": "publish"
}).encode()

req = urllib.request.Request(
    REST_URL,
    data=data,
    headers={
        "Content-Type": "application/json",
        "Cookie": cookies,
        "X-WP-Nonce": nonce,
        "Referer": "https://shaishalin.wordpress.com/wp-admin/post-new.php?post_type=page",
    }
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        print(f"✅ 頁面建立成功！")
        print(f"   標題：{result.get('title', {}).get('rendered', '')}")
        print(f"   URL：{result.get('link', '')}")
except Exception as e:
    print(f"❌ 建立失敗：{e}")
    if hasattr(e, 'read'):
        print(e.read().decode())
