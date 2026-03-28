#!/bin/bash
# AI 創業文章工廠 — 全自動化 SEO 文章生成腳本
# 使用方法: bash scripts/ai-article-factory.sh
# Cron 範例: 每週三自動執行一次

WORKSPACE="/Users/lingo/.openclaw/workspace/shaishalin"
COOKIES="/tmp/wp_cookies.txt"
ARTICLES_DIR="$WORKSPACE/projects/articles"
LOG="$WORKSPACE/logs/article-factory.log"

mkdir -p "$ARTICLES_DIR" "$WORKSPACE/logs"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"
}

log "=== AI 創業文章工廠啟動 ==="

# 檢查 cookie
if [ ! -f "$COOKIES" ]; then
  log "❌ Cookie 檔案不存在，請先在瀏覽器登入 WordPress"
  exit 1
fi

# 文章主題庫（AI 可根據這些主題生成文章）
TOPICS=(
  "AI工具|5個免費AI工具讓你創業效率提升300%|2026年最适合创业者的免费AI工具推荐|AI工具"
  "被動收入|从零建立被动收入的7个步骤|如何用AI工具建立被动收入流|被动收入"
  "聯盟行銷|新手如何開始聯盟行銷：完整指南|聯盟行銷讓你的網站變現|變現策略"
  "數位商品|如何用零成本創建數位商品|从创意到收入：数字商品变现完整攻略|變現策略"
  "內容創作|創業者如何用AI每週產出10篇內容|AI輔助內容創作的正確姿勢|內容行銷"
  "時間管理|創業者時間管理的7個核心原則|如何用Notion追蹤你的創業目標|生產力"
  "SEO|創業者必須知道的10個SEO基礎知識|如何用AI工具做關鍵字研究|SEO優化"
  "Email行銷|如何用Kit建立自動化Email行銷漏斗|Email行銷讓營收自動滾動|Email行銷"
)

# 隨機選擇一個主題
TOPIC=${TOPICS[$((RANDOM % ${#TOPICS[@]}))]}
IFS='|' read -ra PARTS <<< "$TOPIC"
CATEGORY="${PARTS[0]}"
TITLE="${PARTS[1]}"
META_DESC="${PARTS[2]}"
TAG="${PARTS[3]}"

log "📝 主題：$CATEGORY"
log "📌 標題：$TITLE"

# 生成 HTML 文章內容（完整的 WordPress 可用 HTML）
ARTICLE_CONTENT="<!DOCTYPE html>
<html lang=\"zh-TW\">
<head>
<meta charset=\"UTF-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
<title>$TITLE</title>
<meta name=\"description\" content=\"$META_DESC\">
<style>
body { font-family: 'Noto Sans TC', sans-serif; max-width: 720px; margin: 0 auto; padding: 2rem 1rem; line-height: 1.8; color: #333; }
h1 { font-size: 1.8rem; margin-bottom: 1rem; color: #1a1a2e; }
h2 { font-size: 1.3rem; margin: 1.5rem 0 0.75rem; color: #16213e; }
p { margin-bottom: 1rem; }
blockquote { border-left: 4px solid #a78bfa; margin: 1.5rem 0; padding: 0.75rem 1rem; background: #f8f8ff; }
ul { margin: 1rem 0; padding-left: 1.5rem; }
li { margin-bottom: 0.5rem; }
.cta { background: linear-gradient(135deg,#1e1b4b,#312e81); color: #fff; padding: 1.5rem; border-radius: 12px; text-align: center; margin: 2rem 0; }
.cta a { color: #a78bfa; }
</style>
</head>
<body>
<h1>$TITLE</h1>

<p>$META_DESC。在這篇文章中，我會分享具體的策略和可執行的步驟，讓你今天就能開始行動。</p>

<h2>為什麼這個方法有效</h2>
<p>創業者最常見的錯誤是「過度準備才開始」。但現實是，開始才是最重要的。你不需要等到一切都完美，只需要：</p>
<ul>
<li>一個明確的方向</li>
<li>一個最小可行的產品或服務</li>
<li>持續執行並根據市場回饋迭代</li>
</ul>

<h2>核心步驟</h2>
<p>以下是我的核心方法論，經過多個成功案例驗證：</p>

<h3>第一步：確認你的切入點</h3>
<p>不要想「我要做一個很棒的產品」，要想「誰有什麼問題，我可以幫忙解決？」從問題出發，而不是從產品出發。</p>

<h3>第二步：建立一個最小可行產品</h3>
<p>不需要完美。一個簡單的著陸頁、一個 PDF、一個電子郵件課程——都可以是你的第一個產品。重點是：開始收到市場回饋。</p>

<h3>第三步：自動化你的銷售流程</h3>
<p>當你有了第一個產品，就要把銷售流程自動化。這樣你就可以專注在最有價值的事情上——創造更好的產品。</p>

<h3>第四步：持續擴張</h3>
<p>當一個產品的銷售穩定後，就開始擴張第二個、第三個產品線。不要一次做太多，但也不要停在原點。</p>

<blockquote>
「不要浪費時間在完美計劃上。開始行動，在市場中學習和迭代。」— 殺手林
</blockquote>

<h2>結論</h2>
<p>創業不是一個巨大的決定，而是無數個小選擇的累積。每一個正確的小選擇，都會讓你的事業更接近成功。</p>
<p>如果你覺得這篇文章有價值，歡迎分享給其他想要創業的朋友。</p>

<div class=\"cta\">
<p><strong>想要系統化學習創業技能？</strong></p>
<p><a href=\"https://ko-fi.com/s/00367ecd74\">👉 查看殺手林 AI 創業工具包</a></p>
</div>

</body>
</html>"

# 保存文章到本地
FILENAME="$(date '+%Y-%m-%d')-$(echo "$CATEGORY" | tr '[:upper:]' '[:lower:]').html"
echo "$ARTICLE_CONTENT" > "$ARTICLES_DIR/$FILENAME"
log "✅ 文章已保存：$FILENAME"

# 嘗試發布到 WordPress（需要管理員認證）
# 由於 WordPress.com OAuth 限制，這部分需要在瀏覽器中完成
log "📤 文章已準備就緒，請在瀏覽器中發布到 WordPress"
log "📁 文章位置：$ARTICLES_DIR/$FILENAME"

log "=== 文章工廠完成 ==="
