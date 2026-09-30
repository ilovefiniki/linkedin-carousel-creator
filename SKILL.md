---
name: linkedin-carousel-creator
description: Generate high-converting, website-grade LinkedIn carousel PDFs (1080×1350 portrait slides) for Vitaliy's posts. Features rich infographic archetypes (KPI metrics, Legacy vs AI-Native comparison grids, numbered step pipelines, 2x2 quadrants, architecture flows), automatic brand logo detection (n8n, OpenAI, Claude, Figma, etc.), and ILF Studio 2.0 aesthetics. Use whenever the user asks for carousels, slide presentations, or converting posts into swipeable PDFs.
---

# LinkedIn Carousel Creator v2 (Studio-Grade Infographics)

Generates vector PDF carousels (1080×1350 portrait) from LinkedIn posts or structured outlines using a modern Playwright HTML/CSS rendering engine.

**Fixed brand identity & aesthetics** (inspired by `ilf-studio.com 2.0`):
- Author: Vitaliy Alhimovich (AI Engineer)
- Avatar: `/Users/vit/PROJECTS/Shared Skills/.agents/skills/quote_image_creator/assets/avatar.jpg`
- Palette (Dark): Obsidian Dark `#12100E`, Cards `#1C1916`, Borders `#2D261E`, Terracotta Accent `#CC7A3E`, Emerald `#34D399`, Cream `#FAF5EB`
- Palette (Paper): Warm Paper `#EFE8DC`, Cards `#FFFFFF`, Terracotta Accent `#C2531A`, Dark Text `#1B1917`
- Typography: `Plus Jakarta Sans` / `Geist` + `JetBrains Mono`
- Automatic Brand Logos: n8n, OpenAI, Claude, Figma, PostgreSQL, Docker, Python, GitHub, Slack, Stripe, Airtable, HubSpot, etc.

---

## Visual Infographic Archetypes

The generator supports dedicated visual layouts that replace walls of text with authentic graphics:

1. **`cover`**: Bold hook slide (70px bold typography with terracotta highlights), category pill (`[SYSTEMS ENGINEERING • 2026]`), author header, and swipe teaser.
2. **`donut` / `donut_chart`**: Pure vector SVG Donut Chart with glowing segments, center KPI callout (`90% COMMODITIZED`), and color-coded legend cards with mini progress bars.
3. **`metric_bars`**: Horizontal comparison progress meters (`160 hrs` vs `45 hrs` vs `3.5 hrs`) with colored gradient tracks and delta callout (`-98%`, `40x FASTER`).
4. **`ecosystem` / `integration`**: Visual pipeline with **prominent 72px glass brand circles** (Figma, Claude, n8n, PostgreSQL) connected by protocol arrows (`REST API`, `Webhook`, `Direct SQL`).
5. **`visual_hero`**: Editorial 3D AI-generated illustrations or photo cutouts with floating glass telemetry badges (`HETZNER VPS • 24/7 RUNTIME`, `99.98% UPTIME`) and bullet points.
6. **`pyramid` / `hierarchy`**: McKinsey / Minto 3-Tier Hierarchy mental model pyramid.
7. **`comparison`**: Bento comparison grid (`LEGACY` with red pills/crosses vs `AI-NATIVE` with green pills/checks).
8. **`pipeline`**: Numbered horizontal/vertical stepper (`01 -> 02 -> 03 -> 04`) with badges and action summaries.
9. **`quadrant`**: 2×2 mental model matrix cards with numbered badges and punchy takeaways.
10. **`cta`**: Executive summary checklist, hero author card with verified avatar, and fixed non-wrapping bookmarking button (`📌 Save for later`).

---

## Generation Commands

### Option A: Advanced Infographic Mode (`--slides-file` JSON)
For maximum visual impact with diagrams, KPIs, comparisons, and step pipelines:

```bash
python3 "/Users/vit/PROJECTS/Shared Skills/.agents/skills/linkedin_carousel_creator/scripts/generate_carousel_v2.py" \
  --slides-file "/path/to/slides.json" \
  --slug "my-carousel-slug" \
  --output-dir "/Users/vit/PROJECTS/Social Media posting/carousels/" \
  --theme dark
```

### Option B: Quick CLI Mode (Simple text strings or JSON inline)
```bash
python3 "/Users/vit/PROJECTS/Shared Skills/.agents/skills/linkedin_carousel_creator/scripts/generate_carousel_v2.py" \
  --title "Why 90% of AI Automation Fails" \
  --subtitle "And the 3 rules high-performing agencies follow" \
  --slides '["Slide 1 text with n8n and OpenAI", "Slide 2 text with Claude"]' \
  --slug "ai-automation-rules" \
  --output-dir "/Users/vit/PROJECTS/Social Media posting/carousels/" \
  --both-themes
```

---

## Slide JSON Schema Example (`slides.json`)

```json
[
  {
    "archetype": "cover",
    "category": "AGENCY STRATEGY • 2026",
    "title": "Stop Selling Workflows. Sell Systems.",
    "subtitle": "Why single-trigger automations are commoditized and how we build resilient agents."
  },
  {
    "archetype": "kpi",
    "title": "The Brutal Reality of Simple Automation",
    "metric": "84%",
    "metric_label": "OF CLIENT AUTOMATIONS BREAK WITHIN 90 DAYS",
    "items": [
      "API schema drifts break silent webhooks",
      "No state persistence or transactional rollbacks",
      "Clients blame you when third-party tools change payloads"
    ],
    "takeaway": "Reliability is the only moat left in AI development."
  },
  {
    "archetype": "comparison",
    "title": "Legacy Workflows vs AI-Native Infrastructure",
    "legacy_title": "Brittle Zapier / Make Flows",
    "legacy_items": [
      "Rigid sequential branching with fragile regex",
      "Hidden execution timeouts on large files",
      "Manual error triage every Monday morning"
    ],
    "modern_title": "Autonomous Hetzner + n8n Engines",
    "modern_items": [
      "Deterministic database transactions in PostgreSQL",
      "Self-healing error fallback via Claude & Telegram",
      "Dedicated Docker containers under full client ownership"
    ],
    "takeaway": "Shift from being a tool-tweaker to a systems architect."
  },
  {
    "archetype": "pipeline",
    "title": "The 4-Layer Autonomous Delivery Pipeline",
    "steps": [
      {"num": "01", "name": "Event Ingestion", "desc": "Webhook sanitization and honeypot validation with zero unauthenticated drops."},
      {"num": "02", "name": "AI Decision Gate", "desc": "Fast LLM classification (Claude / GPT-4o) with strict Pydantic/JSON schemas."},
      {"num": "03", "name": "Stateful Execution", "desc": "Transactional database storage in PostgreSQL with retry policies."},
      {"num": "04", "name": "Real-time Telemetry", "desc": "Instant Telegram alerts to Vitaliy's phone with 1-click execution overrides."}
    ]
  },
  {
    "archetype": "cta",
    "title": "Want to Build Resilient AI Systems?",
    "items": [
      "Stop competing on price with low-code freelancers",
      "Ship high-performance architectures with zero bloat",
      "Audit every pipeline for schema drift before going live"
    ]
  }
]
```

---

## Brand Logo Auto-Detection & Authentic SVG Protocol

> [!IMPORTANT]
> **Strict Rule on Logos:** NEVER draw or invent company logos with AI generation or handmade SVG sketches. Only use authentic vector SVGs from official brand packages or `simple-icons`.

The engine automatically scans title, subtitle, bullets, and steps for known tech keywords and inserts authentic vector SVG logos in the top corner or inside cards:
- `Anthropic` / `Claude` (official asterisk spark)
- `OpenAI` / `ChatGPT`
- `n8n`
- `Figma`
- `PostgreSQL` / `Postgres`
- `Docker`
- `Python`
- `GitHub`
- `Slack`
- `Stripe`
- `Airtable`
- `HubSpot`
- `Shopify`
- `Telegram`
- `Notion`
- `Google` / `Google Sheets`
- `ILF Studio`

---

## 🎨 Visual Image Generation Rules (Custom Studio Style)

**Never generate generic AI cliché art** (no glowing cyan/purple brains, no blue circuitry lines on dark backgrounds, no synthetic plastic 3D clay figures).

Carousels use two strictly defined visual art styles tailored to the ILF Studio aesthetic:

### Style A: 35mm Cinema Documentary (Photo / Real-World Tech)
Use for showing engineering workspaces, human-in-the-loop workflows, hardware, code environments, and focused production moments (matching the hero video vibe on `ilf-studio.com`).

**Prompt Formula:**
> "Cinematic 35mm film still, shot on Arri Alexa, anamorphic 50mm lens, warm tungsten and soft diffused ambient lighting, deep atmospheric obsidian shadows, subtle Kodak 500T film grain, quiet European editorial documentary aesthetic, authentic studio environment, rich natural textures, filmic color grading with warm highlights, 4:5 vertical aspect ratio, no neon, no 3D render, no plastic sheen."

### Style B: Bauhaus / Dieter Rams Architectural Line Art (Diagrams / Metaphors)
Use for conceptual breakdowns, abstract data flow, technical architecture, and system blueprints.

**Prompt Formula:**
> "Minimalist editorial technical illustration, precision architectural linework, Bauhaus and Dieter Rams aesthetic, warm terracotta #CC7A3E and deep charcoal ink on warm limestone cream background #EFE8DC, subtle risograph texture, Swiss typography poster aesthetic, flat 2D graphic art, technical drafting guides, 4:5 vertical aspect ratio, no 3D, no gradients, no neon."

### 📐 Mandatory Rules for Image Alignment & Framing:
1. **Aspect Ratio & Canvas Proportions:**
   - The visual section is **600px tall** (with ~944px width inside 68px page padding).
   - Generate images in **3:2** (1536×1024) or **16:9** landscape aspect ratio. At 600px height, a 3:2 illustration spans ~900px wide, filling the slide horizontally with perfect balance.
2. **Framing & Borderless Mode (Default):**
   - **Default: Borderless & Seamless** (`border: none`, `background: transparent`). The artwork floats cleanly on the slide background (`#EFE8DC` or `#12100E`) without any artificial bounding boxes, eliminating awkward empty margins or letterbox strips inside a container.
   - **Framed Mode (`framed: true`):** If a bordered card frame is explicitly desired, the container applies `object-fit: cover` so the image fills 100% of the framed section edge-to-edge without letterboxing.
3. **Strict Relevance to Post Content:** The illustration MUST directly reflect the exact technical concept or infrastructure described in the post (e.g., if discussing an API triage router, show an incoming gateway branching into local vs cloud paths, not arbitrary abstract server boxes). Never generate decorative filler.
4. **High Contrast Badge Overlay:** Any badge or pill layered over the image must use the vibrant studio terracotta `#CC7A3E` or white pill with sharp contrast, never dark-on-dark.

---

## Output Artifacts & Previews

Every run produces:
1. `carousel_{slug}.pdf`: Vector 1080×1350 multi-page PDF ready for direct upload to LinkedIn.
2. `previews_carousel_{slug}/slide_XX.png`: High-resolution 2x Retina PNGs for visual inspection in chat or social previewing.

