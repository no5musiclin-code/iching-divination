#!/usr/bin/env node
// 殺手林 Ko-fi 訂單檢查通知系統
// 檢查新訂單並即時通知幫主

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  email: 'linblance@gmail.com',
  appPassword: 'chwe wvdk oeyy wuzx',
  lastOrderFile: path.join(__dirname, '../logs/ko-fi-last-order.txt'),
  logFile: path.join(__dirname, '../logs/ko-fi-orders.log'),
  notifyStateFile: path.join(__dirname, '../logs/ko-fi-last-notify.txt'),
  telegramBotToken: '7813463558:AAF7LKlRV条', // OpenClaw Telegram bot token
  telegramChatId: '8360807447', // Lin Go
};

function log(msg) {
  const ts = new Date().toISOString();
  const line = `[${ts}] ${msg}`;
  console.log(line);
  fs.appendFileSync(CONFIG.logFile, line + '\n');
}

function sendTelegram(message) {
  return new Promise((resolve, reject) => {
    const token = CONFIG.telegramBotToken;
    const chatId = CONFIG.telegramChatId;
    
    if (!token || token.length < 10) {
      log('Telegram bot token not configured, skipping notification');
      resolve(false);
      return;
    }
    
    const data = JSON.stringify({
      chat_id: chatId,
      text: message,
      parse_mode: 'HTML',
    });

    const options = {
      hostname: 'api.telegram.org',
      port: 443,
      path: `/bot${token}/sendMessage`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data),
      },
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          if (result.ok) {
            log('Telegram notification sent successfully');
            resolve(true);
          } else {
            log('Telegram error: ' + body);
            resolve(false);
          }
        } catch (e) {
          log('Telegram parse error: ' + e.message);
          resolve(false);
        }
      });
    });

    req.on('error', (e) => {
      log('Telegram request error: ' + e.message);
      resolve(false);
    });

    req.write(data);
    req.end();
  });
}

async function checkGmailOrders() {
  // 使用 IMAP 檢查 Gmail 最新郵件
  return new Promise((resolve) => {
    const { execSync } = require('child_process');
    
    try {
      // 使用 openssl s_client 連接 Gmail IMAP
      const checkScript = `
set timeout 60
spawn -openclaw
send "A1 LOGIN linblance@gmail.com chwe wvdk oeyy wuzx\\r\\n"
expect "A1 OK"
send "A1 SELECT INBOX\\r\\n"
expect "SELECT"
send "A1 SEARCH SINCE {$(date -v-2H '+%d-%b-%Y')} SUBJECT \\\"ko-fi\\\"\\r\\n"
expect "SEARCH"
send "A1 LOGOUT\\r\\n"
`;
      
      // 簡化：用 python3 檢查
      const { imaplib } = require('imap');
    } catch(e) {}
    
    // 使用 node-imap 或乾脆用 exec
    const pythonCode = `
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta

try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login("linblance@gmail.com", "chwe wvdk oeyy wuzx")
    mail.select('"INBOX"')
    
    now = datetime.now()
    since_date = (now - timedelta(hours=2)).strftime("%d-%b-%Y")
    
    status, messages = mail.search(None, f'SINCE {since_date} SUBJECT "ko-fi"')
    
    orders = []
    if status == 'OK' and messages[0]:
        ids = messages[0].split()
        # 只取最新的 3 封
        for msg_id in ids[-3:]:
            try:
                res, data = mail.fetch(msg_id, '(RFC822)')
                if res == 'OK':
                    msg = email.message_from_bytes(data[0][1])
                    subject, enc = decode_header(msg['Subject'])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(enc or 'utf-8', errors='replace')
                    
                    sender = msg.get('From', '')
                    date = msg.get('Date', '')
                    
                    lower_subj = subject.lower()
                    if any(k in lower_subj for k in ['payment', 'received', 'order', 'thank', 'support', 'purchas', 'you received']):
                        orders.append({
                            'subject': subject,
                            'from': sender,
                            'date': date
                        })
            except Exception as e:
                pass
    
    mail.logout()
    
    if orders:
        print('FOUND_ORDERS')
        import json
        print(json.dumps(orders))
    else:
        print('NO_ORDERS')
        
except Exception as e:
    print('ERROR:' + str(e))
`;
    
    const { execSync } = require('child_process');
    
    try {
      const output = execSync(`python3 -c "${pythonCode.replace(/"/g, '\\"').replace(/\n/g, ' ')}"`, {
        timeout: 30000,
        encoding: 'utf-8',
      });
      
      resolve(output.trim());
    } catch(e) {
      resolve('ERROR: ' + e.message);
    }
  });
}

async function main() {
  log('=== 開始檢查 Ko-fi 訂單 ===');
  
  const result = await checkGmailOrders();
  
  if (result.startsWith('FOUND_ORDERS')) {
    log('🎉 發現新訂單！準備通知幫主！');
    
    // 讀取上次通知時間，避免重複通知
    let lastNotify = '';
    try {
      lastNotify = fs.readFileSync(CONFIG.notifyStateFile, 'utf-8').trim();
    } catch(e) {}
    
    const now = Date.now();
    const notifyKey = result; // 使用郵件內容作為 key
    
    if (lastNotify !== notifyKey) {
      // 第一次發現，立刻發送通知
      const message = `🎉 <b>【Ko-fi 新訂單通知！】</b>

有人購買了你的數位商品！

📦 商品：AI 創業提示詞大全｜50+ 實戰模板
💰 金額：$5 USD（隨喜）
🔗 連結：https://ko-fi.com/s/00367ecd74

快去確認吧！🚀`;

      await sendTelegram(message);
      fs.writeFileSync(CONFIG.notifyStateFile, notifyKey);
      log('✅ 已通知幫主新訂單');
    } else {
      log('已通知過了，跳過');
    }
  } else if (result.startsWith('ERROR')) {
    log('檢查過程出错: ' + result);
  } else {
    log('目前沒有新訂單');
  }
  
  log('=== 檢查完成 ===');
}

main().catch(e => {
  log('Fatal error: ' + e.message);
  process.exit(1);
});
