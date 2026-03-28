/**
 * 殺手林付費牆系統
 * 用法：在任意 HTML 頁面底部加入以下程式碼
 * <script src="shaishalin-paywall.js"></script>
 * <script>initShaishalinPaywall({appName: '易經測字', kofiUrl: 'https://ko-fi.com/s/00367ecd74'});</script>
 */

const _SPW = {
  storageKey: 'shaishalin_unlocked_',
  usesKey: 'shaishalin_uses_',

  init(cfg) {
    this.cfg = cfg || {};
    this.appName = this.cfg.appName || '此工具';
    this.koFiUrl = this.cfg.koFiUrl || 'https://ko-fi.com/s/00367ecd74';
    this.freeUses = this.cfg.freeUses || 3; // 免費使用次數
    this.storageKey = _SPW.storageKey + (this.cfg.id || 'default');
    this.usesKey = _SPW.usesKey + (this.cfg.id || 'default');

    // 檢查是否已解鎖
    if (this.isUnlocked()) {
      this.onUnlocked();
      return;
    }

    // 檢查使用次數
    const uses = this.getUses();
    if (uses >= this.freeUses) {
      this.showPaywall();
    } else {
      this.incrementUses();
      this.onFreeUse(uses + 1);
    }
  },

  isUnlocked() {
    try {
      return localStorage.getItem(this.storageKey) === 'true';
    } catch(e) { return false; }
  },

  getUses() {
    try {
      return parseInt(localStorage.getItem(this.usesKey) || '0', 10);
    } catch(e) { return 0; }
  },

  incrementUses() {
    try {
      const current = this.getUses();
      localStorage.setItem(this.usesKey, String(current + 1));
    } catch(e) {}
  },

  showPaywall() {
    const overlay = document.createElement('div');
    overlay.id = 'spw-overlay';
    overlay.style.cssText = `
      position:fixed;top:0;left:0;right:0;bottom:0;
      background:rgba(10,10,20,0.97);z-index:99999;
      display:flex;align-items:center;justify-content:center;
      font-family:"Noto Sans TC",-apple-system,sans-serif;
    `;
    overlay.innerHTML = `
      <div style="
        background:linear-gradient(135deg,#1a1a2e,#16213e);
        border:1px solid rgba(167,139,250,0.4);
        border-radius:20px;padding:2.5rem;
        max-width:480px;width:90%;text-align:center;
      ">
        <div style="font-size:3rem;margin-bottom:1rem;">🔒</div>
        <h2 style="font-size:1.5rem;color:#e2e8f0;margin-bottom:0.75rem;">
          你已使用 ${this.freeUses} 次免費额度
        </h2>
        <p style="color:#94a3b8;font-size:0.95rem;line-height:1.7;margin-bottom:1.5rem;">
          解鎖完整版，繼續使用這個工具，並獲得所有進階功能。
        </p>
        <div style="
          background:rgba(255,255,255,0.04);
          border-radius:12px;padding:1.25rem;
          margin-bottom:1.5rem;text-align:left;
        ">
          <h3 style="color:#a78bfa;font-size:0.9rem;margin-bottom:0.75rem;">✨ 完整版包含</h3>
          <ul style="list-style:none;padding:0;margin:0;">
            <li style="color:#94a3b8;font-size:0.88rem;padding:0.35rem 0;padding-left:1.2rem;position:relative;">
              <span style="position:absolute;left:0;color:#4ade80;">✓</span>
              不受限的使用次數
            </li>
            <li style="color:#94a3b8;font-size:0.88rem;padding:0.35rem 0;padding-left:1.2rem;position:relative;">
              <span style="position:absolute;left:0;color:#4ade80;">✓</span>
              完整歷史記錄保存
            </li>
            <li style="color:#94a3b8;font-size:0.88rem;padding:0.35rem 0;padding-left:1.2rem;position:relative;">
              <span style="position:absolute;left:0;color:#4ade80;">✓</span>
              PDF 報告下載
            </li>
            <li style="color:#94a3b8;font-size:0.88rem;padding:0.35rem 0;padding-left:1.2rem;position:relative;">
              <span style="position:absolute;left:0;color:#4ade80;">✓</span>
              無廣告干擾
            </li>
          </ul>
        </div>
        <div style="font-size:2.2rem;font-weight:700;color:#a78bfa;margin-bottom:0.25rem;">
          $5 <span style="font-size:1rem;color:#64748b;text-decoration:line-through;margin-left:0.5rem;">$25</span>
        </div>
        <p style="color:#64748b;font-size:0.8rem;margin-bottom:1.5rem;">
          一次付款，永久使用。持續更新。
        </p>
        <a href="${this.koFiUrl}" style="
          background:linear-gradient(135deg,#a78bfa,#7c3aed);
          color:#fff;padding:0.9rem 2rem;border-radius:30px;
          font-weight:700;font-size:1rem;text-decoration:none;
          display:inline-block;transition:transform 0.2s;
        " target="_blank" rel="noopener">
          🚀 立刻解鎖完整版
        </a>
        <p style="color:#64748b;font-size:0.82rem;margin-top:1rem;">
          <a href="${this.koFiUrl}" style="color:#a78bfa;text-decoration:none;" target="_blank" rel="noopener">
            查看完整商品內容 →
          </a>
        </p>
      </div>
    `;
    document.body.appendChild(overlay);
    this.disablePageScroll();
  },

  disablePageScroll() {
    document.body.style.overflow = 'hidden';
    document.addEventListener('touchmove', this.preventScroll, { passive: false });
  },

  preventScroll(e) { e.preventDefault(); },

  onUnlocked() {
    // 工具啟動並處於已解鎖狀態
    const event = new CustomEvent('spw-unlocked', { detail: { app: this.appName } });
    document.dispatchEvent(event);
  },

  onFreeUse(count) {
    // 免費使用提示
    const remaining = this.freeUses - count;
    if (remaining > 0 && remaining <= 2) {
      this.showToast(`📊 免費剩餘 ${remaining} 次，完整版 $5 永久解鎖 →`);
    }
    const event = new CustomEvent('spw-free-use', {
      detail: { app: this.appName, uses: count, remaining }
    });
    document.dispatchEvent(event);
  },

  showToast(msg) {
    const t = document.createElement('div');
    t.textContent = msg;
    t.style.cssText = `
      position:fixed;bottom:20px;left:50%;transform:translateX(-50%);
      background:rgba(167,139,250,0.9);color:#fff;
      padding:0.7rem 1.5rem;border-radius:25px;
      font-size:0.85rem;z-index:99998;white-space:nowrap;
      font-family:"Noto Sans TC",sans-serif;
    `;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 4000);
  }
};

// 初始化函數
function initShaishalinPaywall(config) {
  _SPW.init(config);
}

// 解鎖確認（用戶付款後可在瀏覽器 console 執行此函數）
function unlockShaishalinPaywall(appId) {
  const key = 'shaishalin_unlocked_' + (appId || 'default');
  localStorage.setItem(key, 'true');
  location.reload();
}
