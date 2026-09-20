# 📑 LinkedIn Carousel Creator

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Compatible with AI Agents](https://img.shields.io/badge/AI%20Agents-Claude%20%7C%20Antigravity%20%7C%20Cursor-black)](#)

Generate publication-ready, beautifully typeset PDF carousels (1080×1350 portrait slides) for **LinkedIn** from plain text or outlines in a single command.

No design tools, no Canva subscriptions, no Figma export hassles. Perfect for engineering breakdowns, case studies, and thought leadership.

Part of the **[ILF Studio](https://ilf-studio.com)** & **[ilovefiniki.com](https://ilovefiniki.com)** AI engineering toolset.

---

## ⚡ Quickstart

### 1. Installation
```bash
git clone https://github.com/ilovefiniki/linkedin-carousel-creator.git
cd linkedin-carousel-creator
pip install pillow reportlab
```

### 2. Generate a Carousel
```bash
python3 scripts/generate_carousel.py \
  --title "How to Build AI-Native Web Platforms" \
  --eyebrow "SYSTEM ARCHITECTURE" \
  --slug "ai-native-platforms" \
  --slides '[
    "1. Sub-100ms TTFB\n\nEliminate server-side CMS bloat. Use Astro or Fastify with streaming SSR.",
    "2. Semantic JSON-LD\n\nEnsure data is machine-readable so AI search engines cite your platform directly.",
    "3. Autonomous Verification\n\nRun pre-commit checks with zero console error tolerance."
  ]'
```

Output: `./carousels/ai-native-platforms_YYYY-MM-DD/carousel.pdf`

---

## 🎨 Aesthetic Themes

- **Dark Mode (Default):** Deep slate `#0B0F17` background with crisp white typography and terracotta accents.
- **Paper Theme:** Warm editorial paper `#F8F6F1` with dark ink typography.
- **Cream Theme:** Architectural limestone `#EFE8DC` with dark graphite contrasts.

Run `--both-themes` to render both dark and light PDF editions at once.

---

## 🤖 Use as an AI Agent Skill

Install into your agent workspace:

```bash
# Antigravity & Gemini:
mkdir -p .agents/skills/linkedin-carousel-creator && curl -fsSL https://raw.githubusercontent.com/ilovefiniki/linkedin-carousel-creator/main/SKILL.md -o .agents/skills/linkedin-carousel-creator/SKILL.md

# Claude Code:
mkdir -p .claude/skills/linkedin-carousel-creator && curl -fsSL https://raw.githubusercontent.com/ilovefiniki/linkedin-carousel-creator/main/SKILL.md -o .claude/skills/linkedin-carousel-creator/SKILL.md
```

---

## 📄 License

Released under the [MIT License](LICENSE). Maintained by [Vitaliy Alhimovich](https://github.com/ilovefiniki) at [ILF Studio](https://ilf-studio.com).
