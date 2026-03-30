# YouTube Factory — AI Faceless Video Automation System

**Author:** 殺手林 (Shaishalin)  
**Purpose:** Build faceless YouTube channels automatically using AI + Python  
**Cost:** $0 (100% free tools, no API keys required)  
**Platform:** macOS (uses built-in `say` command + FFmpeg + MoviePy)

---

## Quick Start

```bash
cd scripts
python3 run_pipeline.py --niche iching --count 3
```

## Supported Niches

| Niche | Description | RPM Potential |
|-------|-------------|---------------|
| `iching` | Ancient Chinese wisdom for entrepreneurs | ⭐⭐⭐⭐⭐ |
| `numerology` | Life path and destiny numbers | ⭐⭐⭐⭐ |
| `aitools` | AI tool reviews and tutorials | ⭐⭐⭐⭐ |
| `ancientwisdom` | Lao Tzu, Confucius, Sun Tzu teachings | ⭐⭐⭐⭐⭐ |
| `passiveincome` | Side hustles and investing | ⭐⭐⭐⭐ |

## System Architecture

```
run_pipeline.py
├── script_generator.py    → AI-powered script creation
├── tts_engine.py          → macOS native TTS → MP3
└── video_generator.py     → MoviePy + FFmpeg video rendering
```

## Requirements

- macOS (for built-in `say` TTS)
- Python 3.9+
- FFmpeg (brew install ffmpeg)
- MoviePy (pip install moviepy)
- Pillow (pip install pillow)

## Features

- **5 Niche Channels** with custom script templates
- **Multi-language TTS** (EN, ZH, JA, KO)
- **Premium Visual Design** (dark + gold theme)
- **Ken Burns Effects** on backgrounds
- **Subtitle Overlays** on every frame
- **Batch Generation** (produce multiple videos at once)
- **YouTube API Ready** (requires API key for upload)

## Monetization

1. **YouTube AdSense** — $2-8 CPM (spirituality niche)
2. **Affiliate Links** — Books, courses, tools in descriptions
3. **Digital Products** — Drive traffic to Gumroad/Ko-fi
4. **Sponsored Videos** — $100-500/video after 10K subscribers

## License

MIT — Free to use, modify, and monetize.
