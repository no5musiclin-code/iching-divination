#!/bin/bash
# 殺手林 每週備份寄送腳本
# 寄送完整備份至 no5mmusic.lin@gmail.com

GMAIL="linblance@gmail.com"
APP_PASS="chwe wvdk oeyy wuzx"
BACKUP_FILE="/Users/lingo/.openclaw/workspace/shaishalin/backup/shaishalin-backup-full.md"
RECIPIENT="no5music.lin@gmail.com"

# 讀取備份內容
BODY=$(cat "$BACKUP_FILE")

# 取得本週日期
DATE=$(date +"%Y-%m-%d")

# 寄送郵件
python3 ~/.openclaw/skills/send_gmail/send_gmail.py \
  --receiver "$RECIPIENT" \
  --subject "🔐 殺手林每週備份 - $DATE" \
  --body "$BODY"

echo "備份已寄送至 $RECIPIENT"
