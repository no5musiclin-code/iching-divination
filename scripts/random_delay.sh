#!/bin/bash
# 隨機延遲腳本 - 模擬人類操作節奏
# 用法: source random_delay.sh [最小秒數] [最大秒數]

MIN_DELAY=${1:-3}
MAX_DELAY=${2:-12}

# 隨機延遲
random_delay() {
    DELAY=$((RANDOM % (MAX_DELAY - MIN_DELAY + 1) + MIN_DELAY))
    echo "[隨機等待] ${DELAY} 秒..."
    sleep $DELAY
}

# 人類化打字速度（適用於需要输入的场景）
random_typing_delay() {
    # 每個字元隨機延遲 0.05-0.25 秒
    echo "typing..."
}

random_delay
