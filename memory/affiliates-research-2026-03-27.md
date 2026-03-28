# 聯盟平台 & Stripe 替代方案研究報告
日期：2026-03-27

---

## 任務 1：聯盟計劃申請結果

### 1. Awin
- **URL:** https://ui.awin.com/publisher-signup/us/awin/step1
- **申請狀態:** 複雜流程，需要 Framer 帳號
- **重要發現:** Awin 已收購 ShareASale (2017) 和 ClickBank。現在所有新 publisher 申請都透過 Awin 的統一是台。申請流程：
  1. 填寫公司名稱、稅務居住地（支援 Taiwan）、姓名、Email、密碼
  2. 選擇推廣類型（Content Creators & Influencers 等）
  3. 填寫推廣空間
  4. Email 驗證
- **問題:** 密碼強度 API 回傳 422 錯誤，且整個流程最終導向 Framer 登入頁面
- **支援台灣:** ✅ 稅務居住地有 Taiwan 選項
- **結論:** 申請複雜，需人工介入完成

### 2. Impact.com
- **URL:** https://app.impact.com/signup/none/V2/create-new-mediapartner-account-flow.ihtml
- **申請狀態:** 申請表已開始填寫（姓名、用户名、Email、手機號碼），但無法完成
- **重要發現:** Impact.com 的「Get Started」按鈕會跳轉到 Awin。兩平台已整合。
- **問題:** 需要 SMS 電話驗證碼，無法自動化完成
- **支援台灣:** ✅ 申請表有電話欄位（+886）
- **結論:** 需要真實手機號碼接收 SMS，無法自動化

### 3. ShareASale
- **URL:** https://www.shareasale.com/info/affiliate-program.cfm
- **申請狀態:** 跳轉到 Awin
- **重要發現:** ShareASale 自 2017 年被 Awin 收購，現在已是同一平台
- **結論:** 申請等同 Awin，見上方

### 4. ClickBank
- **URL:** https://accounts.clickbank.com/master/create-account
- **申請狀態:** 申請表已找到並開始填寫
- **流程:** 兩步驟（基本資料 → 條款同意 → 完成）
- **重要欄位:** Country（Taiwan 有）、First Name、Last Name、Phone（+886）、Email、密碼
- **密碼要求:** 至少 2 小寫 + 2 大寫 + 2 數字 + 2 特殊符號，限 32 字元
- **問題:** 瀏覽器互動複雜，表單會因超時重置
- **支援台灣:** ✅
- **結論:** 有獨立的申請流程，但需要較多時間手動完成

### 5. CJ Affiliate
- **URL:** https://public.cj.com/signup/publisher
- **申請狀態:** 申請表已找到
- **表單欄位:** Language、Country、Email、Password、Confirm Password
- **問題:** reCAPTCHA 顯示「site is exceeding its quota」警告，無法通過驗證
- **支援台灣:** 可能（Country 下拉選單待確認）
- **結論:** reCAPTCHA 阻擋自動化申請

---

## 任務 2：Stripe 替代方案研究

### 1. Paddle
- **URL:** https://www.paddle.com/
- **特點:**
  - 訂閱、支付、稅務一站式服務
  - 承擔 chargeback 和 fraud 責任
  - 處理全球銷售稅
  - 4% + $0.40/筆交易
  - 無月費
- **審批難度:** 中等，需審核
- **台灣/香港支援:** 未明確說明，但強調全球合規
- **適合產品:** SaaS、數位商品、應用程式
- **結論:** 比 Stripe 更易用，審批較 Stripe 容易，但費用較高

### 2. Gumroad
- **URL:** https://gumroad.com/
- **特點:**
  - 創作者友好
  - 有附屬計劃（Gumroad 自己的 affiliate program）
  - 免費開始
- **審批難度:** 極容易
- **台灣/香港支援:** ✅ 支援
- **適合產品:** 數位商品、課程、电子书、模板
- **結論:** 最容易上手的選項，適合小型創作者

### 3. Stan (stan.gg)
- **URL:** https://www.stan.gg/
- **狀態:** ❌ 騙局/域名停放頁
- **實際:** stan.gg 是 BrandBucket 的域名銷售頁面，不是實際平台
- **結論:** 不是真實平台，忽略

### 4. Polar
- **URL:** https://polar.sh/
- **特點:**
  - 軟體貨幣化平台
  - 使用量計費 (usage-based billing)
  - 4% + $0.40/筆（含稅務合規、fraud protection）
  - 無月費
  - 專為開發者/軟體設計
- **審批難度:** 低（線上即可申請）
- **台灣/香港支援:** 強調全球稅務合規
- **適合產品:** SaaS 軟體、開發者工具
- **結論:** 現代化選擇，費用透明，適合軟體產品

---

## 建議總結

### 聯盟平台申請優先順序:
1. **ClickBank** - 有獨立流程，相對容易接觸
2. **CJ Affiliate** - 大型平台，但 reCAPTCHA 是障礙
3. **Awin/Impact/ShareASale** - 已整合為同一平台，需透過 Framer 完成

### Stripe 替代方案建議:
1. **Gumroad** - 最容易上手，適合快速開始
2. **Polar** - 適合軟體/開發者產品，費用透明
3. **Paddle** - 較成熟的選項，適合認真發展的 SaaS

---

*研究完成時間：2026-03-27 03:40 GMT+8*
