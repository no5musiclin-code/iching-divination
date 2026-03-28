#!/usr/bin/env python3
"""
易經視覺圖卡生成器 - Pinterest 推廣用
生成 1000x1500 像素 PNG 圖卡，暗色背景 + 金色元素
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# === 設定 ===
OUTPUT_DIR = "/Users/lingo/.openclaw/workspace/shaishalin/projects/pinterest-assets"
WIDTH = 1000
HEIGHT = 1500

# 顏色
BG_COLOR = (10, 10, 15)          # 深黑 #0a0a0f
BG_COLOR_ALT = (26, 10, 46)       # 深紫 #1a0a2e
GOLD = (212, 175, 55)             # 金色 #d4af37
GOLD_LIGHT = (240, 210, 100)       # 淺金
WHITE = (255, 255, 255)
GRAY = (120, 120, 140)

# 易經卦象（64卦部分）
HEXAGRAMS = [
    "䷀", "䷁", "䷂", "䷃", "䷄", "䷅", "䷆", "䷇",
    "䷈", "䷉", "䷊", "䷋", "䷌", "䷍", "䷎", "䷏",
    "䷐", "䷑", "䷒", "䷓", "䷔", "䷕", "䷖", "䷗",
    "䷘", "䷙", "䷚", "䷛", "䷜", "䷝", "䷞", "䷟",
    "䷠", "䷡", "䷢", "䷣", "䷤", "䷥", "䷦", "䷧",
    "䷨", "䷩", "䷪", "䷫", "䷬", "䷭", "䷮", "䷯",
    "䷰", "䷱", "䷲", "䷳", "䷴", "䷵", "䷶", "䷷",
    "䷸", "䷹", "䷺", "䷻", "䷼", "䷽", "䷾", "䷿"
]

# 八經卦符號
TRIGRAMS = ["☰", "☱", "☲", "☳", "☴", "☵", "☶", "☷"]

# 30+ 主題定義
TOPICS = [
    {"num": "01", "en": "Divination Questions", "jp": "測字問事", "zh": "測字問事"},
    {"num": "02", "en": "Love & Relationships", "jp": "愛情占卜", "zh": "愛情占卜"},
    {"num": "03", "en": "Career & Business", "jp": "事業發展", "zh": "事業發展"},
    {"num": "04", "en": "Investment & Money", "jp": "投資理財", "zh": "投資理財"},
    {"num": "05", "en": "Startup Guidance", "jp": "創業指導", "zh": "創業指導"},
    {"num": "06", "en": "Decision Making", "jp": "抉擇困難", "zh": "抉擇困難"},
    {"num": "07", "en": "Relocation", "jp": "搬家遷居", "zh": "搬家遷居"},
    {"num": "08", "en": "Exams & Study", "jp": "考試學業", "zh": "考試學業"},
    {"num": "09", "en": "Health & Wellness", "jp": "健康生活", "zh": "健康生活"},
    {"num": "10", "en": "Social Relationships", "jp": "人際關係", "zh": "人際關係"},
    {"num": "11", "en": "Job Change", "jp": "工作轉職", "zh": "工作轉職"},
    {"num": "12", "en": "Partnership", "jp": "合作共贏", "zh": "合作共贏"},
    {"num": "13", "en": "Marriage & Romance", "jp": "婚姻感情", "zh": "婚姻感情"},
    {"num": "14", "en": "Startup Direction", "jp": "創業方向", "zh": "創業方向"},
    {"num": "15", "en": "Financial Freedom", "jp": "財務自由", "zh": "財務自由"},
    {"num": "16", "en": "Daily Fortune", "jp": "每日運勢", "zh": "每日運勢"},
    {"num": "17", "en": "Lucky Directions", "jp": "幸運方位", "zh": "幸運方位"},
    {"num": "18", "en": "Business Partners", "jp": "創業夥伴", "zh": "創業夥伴"},
    {"num": "19", "en": "Brand Naming", "jp": "品牌命名", "zh": "品牌命名"},
    {"num": "20", "en": "Market Expansion", "jp": "市場擴張", "zh": "市場擴張"},
    {"num": "21", "en": "Product Launch", "jp": "產品上市", "zh": "產品上市"},
    {"num": "22", "en": "Crisis Management", "jp": "危機處理", "zh": "危機處理"},
    {"num": "23", "en": "Brand Strategy", "jp": "品牌策略", "zh": "品牌策略"},
    {"num": "24", "en": "Client Acquisition", "jp": "客戶開發", "zh": "客戶開發"},
    {"num": "25", "en": "Team Building", "jp": "團隊組建", "zh": "團隊組建"},
    {"num": "26", "en": "Online Business", "jp": "線上創業", "zh": "線上創業"},
    {"num": "27", "en": "Passive Income", "jp": "被動收入", "zh": "被動收入"},
    {"num": "28", "en": "AI Tools", "jp": "AI 工具", "zh": "AI 工具"},
    {"num": "29", "en": "Digital Transformation", "jp": "數位轉型", "zh": "數位轉型"},
    {"num": "30", "en": "Future Prediction", "jp": "未來預測", "zh": "未來預測"},
    {"num": "31", "en": "Wealth Abundance", "jp": "財富豐盛", "zh": "財富豐盛"},
    {"num": "32", "en": "Spiritual Growth", "jp": "心靈成長", "zh": "心靈成長"},
]

WEBSITE = "https://no5musiclin-code.github.io/iching-divination/"

# 字體大小（根據可用字體動態調整）
def get_font(size):
    """嘗試多個字體路徑"""
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Apple Symbols.ttf",
        "/System/Library/Fonts/NotoSansCJK-Regular.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return ImageFont.load_default()

def draw_gradient_bg(draw, width, height, color1=BG_COLOR, color2=BG_COLOR_ALT):
    """繪製漸變背景"""
    for y in range(height):
        ratio = y / height
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def draw_decorative_lines(draw, width, height):
    """繪製裝飾線條"""
    # 頂部金線
    draw.line([(60, 60), (width-60, 60)], fill=GOLD, width=1)
    draw.line([(60, 62), (width-60, 62)], fill=GOLD_LIGHT, width=1)
    # 底部金線
    draw.line([(60, height-62), (width-60, height-62)], fill=GOLD, width=1)
    draw.line([(60, height-60), (width-60, height-60)], fill=GOLD_LIGHT, width=1)
    # 左側金線
    draw.line([(60, 60), (60, height-60)], fill=GOLD, width=1)
    # 右側金線
    draw.line([(width-60, 60), (width-60, height-60)], fill=GOLD, width=1)

def draw_hexagram_row(draw, hexagrams, y, width, font_size=40):
    """繪製一行卦象"""
    font = get_font(font_size)
    total = len(hexagrams)
    # 分兩行顯示
    spacing = width / (total + 1)
    for i, h in enumerate(hexagrams[:8]):
        x = spacing * (i + 1)
        draw.text((x - font_size/2, y), h, font=font, fill=GOLD_LIGHT, anchor="mm")

def draw_corner_decoration(draw, x, y, size=20):
    """繪製角落裝飾"""
    draw.line([(x, y), (x+size, y)], fill=GOLD, width=2)
    draw.line([(x, y), (x, y+size)], fill=GOLD, width=2)

def generate_card(topic, hexagram_idx, output_path):
    """生成單張圖卡"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 漸變背景（從上到下）
    draw_gradient_bg(draw, WIDTH, HEIGHT)
    
    # 四角裝飾
    s = 40
    draw_corner_decoration(draw, 50, 50, s)
    draw_corner_decoration(draw, WIDTH-50-s, 50, s)
    draw_corner_decoration(draw, 50, HEIGHT-50-s, s)
    draw_corner_decoration(draw, WIDTH-50-s, HEIGHT-50-s, s)
    
    # 外邊框
    draw.rectangle([(50, 50), (WIDTH-50, HEIGHT-50)], outline=GOLD, width=1)
    
    # 頂部卦象行
    hexagrams_shown = TRIGRAMS + HEXAGRAMS[hexagram_idx:hexagram_idx+8]
    draw_hexagram_row(draw, hexagrams_shown, 140, WIDTH, font_size=38)
    
    # 分隔線
    draw.line([(150, 195), (WIDTH-150, 195)], fill=GOLD, width=1)
    
    # 頂部標題（小字）
    font_small = get_font(18)
    title_top = "I CHING · 易經占卜"
    bbox = draw.textbbox((0, 0), title_top, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw)/2, 210), title_top, font=font_small, fill=GOLD)
    
    # 主標題（中文大字）
    font_zh = get_font(72)
    zh_bbox = draw.textbbox((0, 0), topic["zh"], font=font_zh)
    zh_tw = zh_bbox[2] - zh_bbox[0]
    draw.text(((WIDTH - zh_tw)/2, 350), topic["zh"], font=font_zh, fill=WHITE, anchor="lm")
    
    # 英文副標題
    font_en = get_font(32)
    en_bbox = draw.textbbox((0, 0), topic["en"], font=font_en)
    en_tw = en_bbox[2] - en_bbox[0]
    draw.text(((WIDTH - en_tw)/2, 440), topic["en"], font=font_en, fill=GOLD_LIGHT, anchor="lm")
    
    # 日文
    font_jp = get_font(28)
    jp_bbox = draw.textbbox((0, 0), topic["jp"], font=font_jp)
    jp_tw = jp_bbox[2] - jp_bbox[0]
    draw.text(((WIDTH - jp_tw)/2, 492), topic["jp"], font=font_jp, fill=GRAY, anchor="lm")
    
    # 中央大卦象裝飾
    big_hex = HEXAGRAMS[hexagram_idx % 64]
    font_big = get_font(200)
    draw.text((WIDTH/2, 780), big_hex, font=font_big, fill=GOLD, anchor="mm")
    
    # 陰陽裝飾
    font_yinyang = get_font(60)
    draw.text((WIDTH/2 - 200, 880), "☯", font=font_yinyang, fill=GOLD_LIGHT, anchor="mm")
    draw.text((WIDTH/2 + 200, 880), "☯", font=font_yinyang, fill=GOLD_LIGHT, anchor="mm")
    
    # 分隔裝飾線
    for i, ox in enumerate([-150, 0, 150]):
        draw.ellipse([(WIDTH/2 + ox - 4, 970 - 4), (WIDTH/2 + ox + 4, 970 + 4)], fill=GOLD)
    
    # 底部說明文字
    font_desc = get_font(22)
    lines = [
        "探索易經智慧 · 解讀人生方向",
        "64卦洞察 · 指引迷津",
    ]
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_desc)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw)/2, 1010 + i*36), line, font=font_desc, fill=GRAY, anchor="lm")
    
    # 網址
    font_url = get_font(24)
    url_bbox = draw.textbbox((0, 0), WEBSITE, font=font_url)
    url_tw = url_bbox[2] - url_bbox[0]
    draw.text(((WIDTH - url_tw)/2, HEIGHT - 100), WEBSITE, font=font_url, fill=GOLD, anchor="lm")
    
    # 底部卦象小裝飾
    small_hex = HEXAGRAMS[(hexagram_idx + 16) % 64] + " " + HEXAGRAMS[(hexagram_idx + 32) % 64] + " " + HEXAGRAMS[(hexagram_idx + 48) % 64]
    font_small_hex = get_font(28)
    hbbox = draw.textbbox((0, 0), small_hex, font=font_small_hex)
    htw = hbbox[2] - hbbox[0]
    draw.text(((WIDTH - htw)/2, HEIGHT - 60), small_hex, font=font_small_hex, fill=GOLD, anchor="lm")
    
    img.save(output_path, "PNG", quality=95)
    print(f"  ✓ {output_path}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 額外主題（31-32）
    extra_topics = TOPICS[30:]
    
    print(f"開始生成 {len(TOPICS)} 張易經圖卡...")
    print(f"輸出目錄: {OUTPUT_DIR}")
    print()
    
    for i, topic in enumerate(TOPICS):
        hex_idx = i % 64
        filename = f"iching-card-{topic['num']}-{topic['en'].lower().replace(' & ', '-').replace(' ', '-').replace('/', '-')}.png"
        filename = filename.replace("&", "and").replace("/", "-")
        output_path = os.path.join(OUTPUT_DIR, filename)
        generate_card(topic, hex_idx, output_path)
    
    print()
    print(f"✅ 完成！共生成 {len(TOPICS)} 張圖卡")
    print(f"📁 路徑: {OUTPUT_DIR}")
    
    # 列出生成的文件
    files = sorted(os.listdir(OUTPUT_DIR))
    print(f"\n📋 檔案列表 ({len(files)} 個):")
    for f in files:
        print(f"  - {f}")

if __name__ == "__main__":
    main()
