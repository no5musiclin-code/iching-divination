#!/usr/bin/env python3
"""
殺手林 Ko-fi 訂單檢查腳本
檢查 Gmail 是否有新的 Ko-fi 付款通知，有則發 email 通知幫主
"""
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import json
import os
import sys

# 設定
EMAIL = "linblance@gmail.com"
APP_PASSWORD = "chwe wvdk oeyy wuzx"
NOTIFY_TO = "no5music.lin@gmail.com"
LOG_FILE = os.path.join(os.path.dirname(__file__), "../logs/ko-fi-orders.log")
LAST_NOTIFY_FILE = os.path.join(os.path.dirname(__file__), "../logs/ko-fi-last-notify.json")
SEND_GMAIL = os.path.expanduser("~/.openclaw/skills/send_gmail/send_gmail.py")

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except:
        pass

def send_email(subject, body):
    """用 Gmail App Password 寄送通知"""
    import subprocess
    cmd = [
        "python3", SEND_GMAIL,
        "--receiver", NOTIFY_TO,
        "--subject", subject,
        "--body", body
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            log(f"✅ 郵件通知已寄出")
            return True
        else:
            log(f"❌ 郵件寄送失敗: {result.stderr}")
            return False
    except Exception as e:
        log(f"寄送錯誤: {e}")
        return False

def check_orders():
    """檢查 Gmail 是否有 Ko-fi 新訂單"""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(EMAIL, APP_PASSWORD)
        mail.select('"INBOX"')
        
        now = datetime.now()
        # 只檢查最近 30 分鐘內的郵件
        since_date = (now - timedelta(minutes=30)).strftime("%d-%b-%Y")
        
        # 搜索 Ko-fi 相關郵件
        status, messages = mail.search(None, f'SINCE {since_date} SUBJECT "ko-fi"')
        
        new_orders = []
        
        if status == 'OK' and messages[0]:
            for msg_id in messages[0].split():
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
                        # 付款相關關鍵字
                        keywords = ['payment', 'received', 'order', 'thank', 'support', 
                                  'purchas', 'you received', 'new order', 'order confirmed']
                        if any(k in lower_subj for k in keywords):
                            new_orders.append({
                                'subject': subject,
                                'from': sender,
                                'date': date
                            })
                            log(f"發現訂單郵件: {subject}")
                except Exception as e:
                    log(f"讀取郵件錯誤: {e}")
        
        mail.logout()
        return new_orders
        
    except Exception as e:
        log(f"IMAP 連接錯誤: {e}")
        return []

def main():
    log("=== 殺手林 Ko-fi 訂單檢查 ===")
    
    new_orders = check_orders()
    
    if new_orders:
        log(f"🎉 發現 {len(new_orders)} 筆新訂單！")
        
        # 讀取上次通知記錄，避免重複通知
        last_notify = {}
        try:
            if os.path.exists(LAST_NOTIFY_FILE):
                with open(LAST_NOTIFY_FILE, 'r') as f:
                    last_notify = json.load(f)
        except:
            pass
        
        # 檢查每筆新訂單
        for order in new_orders:
            order_key = order['subject'] + '|' + order['date']
            
            if order_key not in last_notify:
                # 新訂單！立刻發送通知
                subject = "🎉 【Ko-fi 新訂單！】AI 創業提示詞大全 - 有人购买了！"
                body = f"""幫主！🎉 新訂單通知！

有人購買了你的數位商品！

📦 商品：AI 創業提示詞大全｜50+ 實戰模板
💰 金額：$5 USD（隨喜價）
🔗 商品連結：https://ko-fi.com/s/00367ecd74
📬 通知時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

快去 Ko-fi 儀表板確認訂單！🚀

— 殺手林 自動通知系統
"""
                send_email(subject, body)
                last_notify[order_key] = datetime.now().isoformat()
                log(f"✅ 已通知幫主: {order['subject']}")
        
        # 更新通知記錄
        try:
            with open(LAST_NOTIFY_FILE, 'w') as f:
                json.dump(last_notify, f, indent=2)
        except:
            pass
    else:
        log("目前沒有新訂單")
    
    log("=== 檢查完成 ===")

if __name__ == "__main__":
    main()
