#!/bin/bash
# 易經多語言網站部署腳本
# 支援：Netlify / Vercel / GitHub Pages / 本地打包

WORKSPACE="/Users/lingo/.openclaw/workspace/shaishalin/projects/iching-deploy"
DEPLOY_DIR="$WORKSPACE/dist"

echo "=== 易經測字多平台部署系統 ==="

# 建立部署目錄
mkdir -p "$DEPLOY_DIR"

# 複製所有版本
echo "📦 打包所有語言版本..."
cp "$WORKSPACE/projects/iching-en/index.html" "$DEPLOY_DIR/iching-en/index.html"
cp "$WORKSPACE/projects/iching-zht/index.html" "$DEPLOY_DIR/iching-zht/index.html"
cp "$WORKSPACE/projects/iching-zhs/index.html" "$DEPLOY_DIR/iching-zhs/index.html"
cp "$WORKSPACE/projects/iching-ja/index.html" "$DEPLOY_DIR/iching-ja/index.html"
cp "$WORKSPACE/projects/iching-deploy/index.html" "$DEPLOY_DIR/index.html"

# 建立 Google sitemap（SEO必備）
cat > "$DEPLOY_DIR/sitemap.xml" << 'SITEMAP'
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://iching.shaishalin.com/iching-en/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>
  <url><loc>https://iching.shaishalin.com/iching-zht/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>
  <url><loc>https://iching.shaishalin.com/iching-zhs/</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>
  <url><loc>https://iching.shaishalin.com/iching-ja/</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>
</urlset>
SITEMAP

# 建立 robots.txt
cat > "$DEPLOY_DIR/robots.txt" << 'ROBOTS'
User-agent: *
Allow: /
Sitemap: https://iching.shaishalin.com/sitemap.xml
ROBOTS

# 建立 Netlify 設定檔
cat > "$DEPLOY_DIR/netlify.toml" << 'NETLIFY'
[build]
  publish = "."

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[redirects]]
  from = "/"
  to = "/iching-zht/"
  status = 302

[[redirects]]
  from = "/en"
  to = "/iching-en/"
  status = 302

[[redirects]]
  from = "/zh"
  to = "/iching-zht/"
  status = 302

[[redirects]]
  from = "/jp"
  to = "/iching-ja/"
  status = 302
NETLIFY

echo "✅ 打包完成！檔案位於：$DEPLOY_DIR"
echo ""
echo "=== 部署選項 ==="
echo ""
echo "1️⃣ Netlify（推薦 — 完全免費，全球CDN）"
echo "   → 前往 https://app.netlify.com/drop"
echo "   → 將 '$DEPLOY_DIR' 資料夾拖入即可"
echo ""
echo "2️⃣ Vercel（推薦 — 免費，部署快）"
echo "   → 運行: vercel --prod '$DEPLOY_DIR'"
echo ""
echo "3️⃣ GitHub Pages"
echo "   → 將 dist/ 資料夾的內容上傳到 GitHub repo"
echo "   → 在 repo Settings → Pages 啟用"
echo ""
echo "4️⃣ 打包成 ZIP（離線部署）"
echo "   → 運行: zip -r iching-deploy.zip '$DEPLOY_DIR'"
echo ""
echo "=== 檔案清單 ==="
ls -la "$DEPLOY_DIR"
echo ""
echo "=== 已就緒！請選擇部署方式 ==="
