const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  
  // Use the same profile as openclaw
  const context = await browser.newContext({
    userDataDir: process.env.HOME + '/Library/Application Support/openclaw-browser/openclaw'
  });
  
  const page = await context.newPage();
  
  try {
    // Go to Ko-fi shop settings
    await page.goto('https://ko-fi.com/shop/settings?productType=0', { timeout: 10000 });
    await page.waitForTimeout(2000);
    
    console.log('Page title:', await page.title());
    
    // Click Add Product
    const addBtn = page.locator('button:has-text("Add Product")');
    await addBtn.click();
    await page.waitForTimeout(1500);
    
    // Step 1: Enter product name
    const nameInput = page.locator('input[placeholder*="Comic PDF"]');
    await nameInput.fill('AI 創業提示詞大全｜50+ 實戰模板');
    await page.waitForTimeout(500);
    
    // Click Next step
    const nextBtn = page.locator('button:has-text("Next step")');
    await nextBtn.click();
    await page.waitForTimeout(1500);
    
    // Step 2: Fill description
    const descInput = page.locator('textarea').first();
    await descInput.fill('50+ 個經過測試的 AI 創業提示詞，涵蓋：商業計劃教練、聯盟行銷文案、SEO 關鍵字工具、銷售漏斗序列、流量變現策略、社群內容日曆。直接複製貼上 ChatGPT、Claude 或 Gemini 使用，適合新手創業者。購買後永久存取。');
    await page.waitForTimeout(300);
    
    // Fill product summary
    const summaryInputs = page.locator('textarea');
    const count = await summaryInputs.count();
    console.log('Found', count, 'textareas');
    if (count >= 2) {
      await summaryInputs.nth(1).fill('50+ AI 創業提示詞 商業行銷變現攻略');
    }
    await page.waitForTimeout(300);
    
    // Set price
    const priceInput = page.locator('input[type="number"]');
    await priceInput.fill('5');
    await page.waitForTimeout(300);
    
    // Click URL redirect option
    const urlRedirectLink = page.locator('text=Redirect buyer to a URL');
    await urlRedirectLink.click();
    await page.waitForTimeout(500);
    
    // Fill redirect URL
    const urlInput = page.locator('input[placeholder*="redirect"]');
    await urlInput.fill('https://shaishalin.wordpress.com/prompts-download');
    await page.waitForTimeout(300);
    
    // Check copyright checkbox
    const copyrightCb = page.locator('input[type="checkbox"]').filter({ has: page.locator('.. >> text=I created') }).first();
    await copyrightCb.check();
    await page.waitForTimeout(300);
    
    // Click Save and publish
    const saveBtn = page.locator('button:has-text("Save and publish")');
    await saveBtn.scrollIntoViewIfNeeded();
    await saveBtn.click();
    await page.waitForTimeout(3000);
    
    console.log('Clicked Save and publish');
    
    // Check for dialog and close it if present
    const dialogCloseBtn = page.locator('[role="dialog"] button:has-text("Close")').first();
    if (await dialogCloseBtn.isVisible({ timeout: 1000 }).catch(() => false)) {
      await dialogCloseBtn.click();
      await page.waitForTimeout(1000);
      await saveBtn.click();
      await page.waitForTimeout(3000);
    }
    
    // Check if we're still on the form or redirected
    const url = page.url();
    console.log('Current URL:', url);
    
    // Check if product was created
    const pageContent = await page.content();
    if (pageContent.includes('AI 創業提示詞大全')) {
      console.log('SUCCESS: Product appears to be created!');
    } else {
      console.log('Product may not have been created, taking screenshot...');
    }
    
    // Take screenshot
    await page.screenshot({ path: '/tmp/ko-fi-result.png', fullPage: true });
    console.log('Screenshot saved to /tmp/ko-fi-result.png');
    
  } catch (e) {
    console.error('Error:', e.message);
    await page.screenshot({ path: '/tmp/ko-fi-error.png' });
  }
  
  await browser.close();
})();
