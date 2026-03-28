#!/bin/bash
# 殺手林 WordPress 每日自動發文 Cron Job 設定腳本
# 使用方式: bash cron-setup.sh

SCRIPT_PATH="/Users/lingo/.openclaw/workspace/shaishalin/scripts/daily-wordpress-post.py"
LOG_PATH="/Users/lingo/.openclaw/workspace/shaishalin/logs/daily-wp-post.log"
CRON_CMD="0 0 * * * /usr/bin/python3 $SCRIPT_PATH --publish >> $LOG_PATH 2>&1"

echo "======================================"
echo "🔮 殺手林 WordPress 每日發文 Cron 設定"
echo "======================================"
echo ""
echo "排程時間：每天 00:00 UTC = 早上 8:00 Asia/Taipei"
echo "執行腳本：$SCRIPT_PATH"
echo "日誌檔案：$LOG_PATH"
echo ""

# 檢查是否已有設定
if crontab -l 2>/dev/null | grep -q "daily-wordpress-post"; then
    echo "⚠️ 每日 WordPress 發文 cron 已存在！"
    echo ""
    crontab -l | grep "daily-wordpress-post"
    echo ""
    echo "若要移除，請使用：crontab -e 並刪除該行"
else
    # 加入新的 cron job
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "✅ Cron job 已新增！"
fi

echo ""
echo "======================================"
echo "📋 目前的每日 WordPress Cron Jobs："
echo "======================================"
crontab -l 2>/dev/null | grep "daily-wordpress-post" || echo "（無）"
