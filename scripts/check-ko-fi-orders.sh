#!/bin/bash
# 殺手林 Ko-fi 訂單檢查腳本
# 檢查新訂單並第一時間通知幫主

LOG_FILE="/Users/lingo/.openclaw/workspace/shaishalin/logs/ko-fi-orders.log"
LAST_CHECK_FILE="/Users/lingo/.openclaw/workspace/shaishalin/logs/ko-fi-last-order.txt"

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 檢查 Ko-fi 訂單中..." >> "$LOG_FILE"

# 使用 curl 檢查 Ko-fi 商店頁面（檢查是否有新訂單）
# Ko-fi 的訂單頁面需要登入，但有另一個方法：檢查付款通知頁面

ORDER_URL="https://ko-fi.com/manage/supportreceived"
NOTIFY_SCRIPT="/Users/lingo/.openclaw/workspace/shaishalin/scripts/send-notify.sh"

# 讀取上次最後訂單 ID
LAST_ORDER_ID=$(cat "$LAST_CHECK_FILE" 2>/dev/null || echo "")

# 這裡我們用瀏覽器自動化檢查
# 但更聰明的方法：直接檢查 email 有沒有付款通知
# 因為 PayPal 付款成功後 Ko-fi 會寄 email

# 讀取 Gmail 最新郵件，檢查是否有新的 Ko-fi 付款通知
python3 << 'EOF'
import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime, timedelta

# 讀取上次的檢查時間
last_check_file = "/Users/lingo/.openclaw/workspace/shaishalin/logs/ko-fi-last-check.txt"
now = datetime.now()

try:
    with open(last_check_file, 'r') as f:
        last_check_str = f.read().strip()
        last_check = datetime.fromisoformat(last_check_str)
except:
    last_check = now - timedelta(hours=24)
    with open(last_check_file, 'w') as f:
        f.write(now.isoformat())

# 連接 Gmail
mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login("linblance@gmail.com", "chwe wvdk oeyy wuzx")
mail.select('"INBOX"')

# 搜索最近 2 小時的 Ko-fi 相關郵件
since_date = (now - timedelta(hours=2)).strftime("%d-%b-%Y")
status, messages = mail.search(None, f'SINCE {since_date} SUBJECT "ko-fi"')

new_order = False
order_details = ""

if status == 'OK':
    for msg_id in messages[0].split():
        try:
            status, msg_data = mail.fetch(msg_id, '(RFC822)')
            if status == 'OK':
                msg = email.message_from_bytes(msg_data[0][1])
                subject, encoding = decode_header(msg['Subject'])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or 'utf-8', errors='replace')
                
                from_addr = msg.get('From', '')
                date_str = msg.get('Date', '')
                
                # 檢查是否是付款/訂單相關
                lower_subject = subject.lower()
                if any(kw in lower_subject for kw in ['payment', 'received', 'order', 'thank', 'support', 'purchas']):
                    new_order = True
                    order_details += f"📧 主旨: {subject}\n"
                    order_details += f"📬 寄件者: {from_addr}\n"
                    order_details += f"🕐 時間: {date_str}\n"
                    order_details += "---\n"
        except Exception as e:
            pass

# 更新最後檢查時間
with open(last_check_file, 'w') as f:
    f.write(now.isoformat())

mail.logout()

if new_order:
    print("NEW_ORDER:" + order_details)
else:
    print("NO_NEW_ORDER")
EOF

result=$?

# 如果 Python 執行出錯
if [ $? -ne 0 ]; then
    echo "[錯誤] 檢查訂單失敗"
    exit 1
fi
