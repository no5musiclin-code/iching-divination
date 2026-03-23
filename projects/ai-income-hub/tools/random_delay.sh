#!/bin/bash
# 隨機延遲腳本 - 人類化操作節奏
MIN=3; MAX=15
DELAY=$((RANDOM % (MAX - MIN + 1) + MIN))
echo "等待 ${DELAY} 秒..."
sleep $DELAY
