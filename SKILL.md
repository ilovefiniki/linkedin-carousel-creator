---
name: linkedin-carousel-creator
description: Generate professional PDF carousels (1080×1350 portrait slides) for LinkedIn from any post, article, or outline. Trigger when user says "make a carousel", "create slides", "generate PDF carousel", "convert post to carousel", or wants to turn a text post into an aesthetic swipeable LinkedIn document.
---

# LinkedIn Carousel Creator

Generates a publication-ready branded PDF carousel (1080×1350 portrait slides) from a LinkedIn post, article, or outline.

---

## ⚡ Quickstart

### Prerequisites
```bash
pip install pillow reportlab
```

### Basic Command
```bash
python3 scripts/generate_carousel.py \
  --title "Why Multi-Agent Systems Fail in Production" \
  --eyebrow "AI ARCHITECTURE · LESSON LEARNED" \
  --slug "agent-failure-modes" \
  --slides '[
    "1. Context Drift\n\nAgents without deterministic boundaries accumulate conversational noise.",
    "2. Ungated Tool Execution\n\nRunning destructive APIs without human verification gates leads to silent failures.",
    "3. Missing Memory Persistence\n\nFailing to synchronize intermediate state across session restarts."
  ]'
```

Produces:
`./carousels/agent-failure-modes_YYYY-MM-DD/carousel.pdf`

---

## 🎨 Design Themes

Supports 3 curated editorial themes:
- `dark` — Deep slate `#0B0F17` with terracotta/cyan highlights (Default).
- `paper` — Editorial warm paper `#F8F6F1` with dark ink typography.
- `cream` — Studio warm limestone `#EFE8DC` with deep slate contrast.

To generate both light and dark versions at once:
```bash
python3 scripts/generate_carousel.py ... --both-themes
```

---

## 🛠️ CLI Flags & Options

| Flag | Default | Description |
|---|---|---|
| `--title` | *(Required)* | Cover slide title. |
| `--slides` | *(Required)* | JSON array of slide strings. |
| `--slug` | *(Required)* | Subfolder name. |
| `--eyebrow` | `None` | Technical mono tag above title (e.g. `CASE STUDY`). |
| `--subtitle` | `None` | Optional subtitle under title on cover. |
| `--name` | `Alex Rivers` | Author name. |
| `--job-title` | `AI Engineer & Systems Architect` | Author headline. |
| `--avatar` | `assets/default_avatar.png` | Author avatar. |
| `--website` | `example.com` | URL on final CTA slide. |
| `--theme` | `dark` | `dark`, `paper`, or `cream`. |
| `--output-dir`| `./carousels` | Destination directory. |
