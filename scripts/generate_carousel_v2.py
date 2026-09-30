#!/usr/bin/env python3
"""
LinkedIn Carousel Generator v2.1 (Studio-Grade Infographics & Visual Canvas Engine)
Engineered for Vitaliy / ILF Studio & ilovefiniki.com.

Features:
- Pixel-perfect 1080×1350 (4:5 portrait) vector PDF output.
- True Visual Infographics:
  1. Donut Charts (Pure vector SVG with glowing segments and legend cards).
  2. Metric Bars (Visual horizontal progress comparison meters with delta badges).
  3. Ecosystem Flow (Prominent 72px brand logo hubs & protocol connectors: Figma, Claude, n8n, Postgres).
  4. Pyramid Hierarchy (McKinsey / Minto 3-tier mental model).
  5. Visual Hero (High-end 3D AI illustrations and photo cutouts with floating stats).
  6. Bento Comparison (Legacy vs AI-Native).
  7. Pipeline Stepper (01 -> 02 -> 03 -> 04).
  8. 2x2 Matrix / Quadrants.
  9. High-converting CTA with non-wrapping button.
- Signature ILF Studio 2.0 Design System (Obsidian Dark with Terracotta #CC7A3E and Warm Paper).
- 2x Retina PNG preview exports.
"""

import argparse
import base64
import json
import math
import os
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSETS_DIR = SKILL_DIR / "assets"
LOGOS_DIR = ASSETS_DIR / "logos"

# Clean helper integration if available
try:
    WM_DIR = SKILL_DIR.parent / "watermarks_remover"
    if str(WM_DIR) not in sys.path:
        sys.path.insert(0, str(WM_DIR))
    from clean_helper import clean_file_path, clean_text_str
except ImportError:
    clean_file_path = None
    clean_text_str = lambda s: s


def load_svg_logo(brand_name: str) -> str:
    """Loads an SVG logo by brand name and returns inline SVG string."""
    alias_map = {
        "chatgpt": "openai",
        "gpt": "openai",
        "gpt4": "openai",
        "gpt-4": "openai",
        "anthropic": "claude",
        "sheets": "googlesheets",
        "google sheets": "googlesheets",
        "docs": "googledocs",
        "google docs": "googledocs",
        "gmail": "gmail",
        "google mail": "gmail",
        "email": "gmail",
        "postgres": "postgresql",
        "psql": "postgresql",
        "ilf": "ilf-studio",
        "tg": "telegram",
    }
    key = alias_map.get(brand_name.lower().strip(), brand_name.lower().strip())
    logo_file = LOGOS_DIR / f"{key}.svg"
    if logo_file.exists():
        try:
            with open(logo_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                # Clean up xml header if present
                content = re.sub(r"<\?xml.*?\?>", "", content, flags=re.DOTALL).strip()
                return content
        except Exception:
            pass
    return ""


def detect_brand_logos(text: str) -> list[tuple[str, str]]:
    """Scans text for brand mentions and returns list of (brand_name, svg_content)."""
    # Tuples of (search_phrase, icon_key)
    brand_mappings = [
        ("google sheets", "googlesheets"),
        ("google docs", "googledocs"),
        ("gmail", "gmail"),
        ("n8n", "n8n"),
        ("openai", "openai"),
        ("claude", "claude"),
        ("figma", "figma"),
        ("postgresql", "postgresql"),
        ("docker", "docker"),
        ("python", "python"),
        ("github", "github"),
        ("hubspot", "hubspot"),
        ("slack", "slack"),
        ("stripe", "stripe"),
        ("whatsapp", "whatsapp"),
        ("shopify", "shopify"),
        ("airtable", "airtable"),
        ("googlesheets", "googlesheets"),
        ("googledocs", "googledocs"),
        ("google", "google"),
        ("make", "make"),
        ("telegram", "telegram"),
        ("notion", "notion")
    ]
    found = []
    seen = set()
    lower_text = text.lower()
    for phrase, brand_key in brand_mappings:
        pattern = rf"\b{re.escape(phrase)}\b"
        if re.search(pattern, lower_text):
            if brand_key not in seen:
                svg = load_svg_logo(brand_key)
                if svg:
                    found.append((brand_key, svg))
                    seen.add(brand_key)
    return found


def image_to_data_uri(path: str) -> str:
    p = Path(path)
    if not p.is_file():
        return ""
    with open(p, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = p.suffix.lower().lstrip(".")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp", "svg": "svg+xml"}.get(ext, "jpeg")
    return f"data:image/{mime};base64,{data}"


def format_accents(text: str, theme: str = "dark") -> str:
    """Highlights key words or wrapped tags with signature terracotta accents."""
    text = clean_text_str(text)
    accent_color = "#CC7A3E"
    # Convert markdown bold **word** to styled span
    styled = re.sub(
        r"\*\*(.*?)\*\*",
        rf'<span class="accent-text" style="color: {accent_color}; font-weight: 700;">\1</span>',
        text
    )
    # Convert `code` to mono badge
    styled = re.sub(
        r"`(.*?)`",
        r'<code class="inline-code">\1</code>',
        styled
    )
    return styled


def generate_svg_donut(segments: list[dict], size: int = 360, stroke_width: int = 42) -> str:
    """Generates an authentic vector SVG donut chart with stroke-dasharray segments."""
    r = (size - stroke_width) / 2
    cx = cy = size / 2
    circumference = 2 * math.pi * r

    total = sum(float(s.get("val", 0)) for s in segments) or 100.0
    current_offset = 0.0

    paths = []
    for s in segments:
        val = float(s.get("val", 0))
        pct = val / total
        dash = pct * circumference
        gap = circumference - dash
        color = s.get("color", "var(--accent)")

        paths.append(f"""
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" 
          stroke-width="{stroke_width}" stroke-dasharray="{dash:.2f} {gap:.2f}" 
          stroke-dashoffset="{-current_offset:.2f}" stroke-linecap="round"/>
        """)
        current_offset += dash

    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" class="donut-svg-graphic">
      <defs>
        <filter id="donut-glow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="8" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
      </defs>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="{stroke_width}"/>
      <g transform="rotate(-90 {cx} {cy})">
        {''.join(paths)}
      </g>
    </svg>
    """


def build_slide_html(slide_data: dict, index: int, total: int, theme: str = "dark", author_data: dict = None) -> str:
    stype = slide_data.get("type") or slide_data.get("archetype") or "editorial"
    title = slide_data.get("title", "")
    content = slide_data.get("content", "")
    subtitle = slide_data.get("subtitle", "")
    badge = slide_data.get("badge", "")

    author = author_data or {}
    avatar_uri = image_to_data_uri(author.get("avatar", ""))
    author_name = author.get("name", "Vitaliy Alhimovich")
    author_title = author.get("title", "AI Engineer | ilf-studio.com")

    # Brand logos in content (chips in top corner for subtle awareness)
    logos = detect_brand_logos(f"{title} {content} {subtitle}")
    logos_html = ""
    if logos and stype not in ("cover", "ecosystem", "integration"):
        items = "".join([f'<div class="brand-chip" title="{name}">{svg}<span>{name}</span></div>' for name, svg in logos[:3]])
        logos_html = f'<div class="brand-bar">{items}</div>'

    # Slide Header Component
    header_html = f"""
    <div class="slide-header">
      <div class="header-left">
        <span class="badge-pill">{badge or "INSIGHT"}</span>
        {logos_html}
      </div>
      <div class="slide-counter">{index:02d} / {total:02d}</div>
    </div>
    """

    # Slide Footer Component
    footer_html = f"""
    <div class="slide-footer">
      <div class="footer-author">
        {f'<img class="footer-avatar" src="{avatar_uri}">' if avatar_uri else ''}
        <div class="footer-meta">
          <span class="footer-name">{author_name}</span>
          <span class="footer-title">{author_title}</span>
        </div>
      </div>
      <div class="swipe-indicator">Swipe →</div>
    </div>
    """

    # ARCHETYPE 1: COVER SLIDE
    if stype == "cover":
        category = slide_data.get("category", "SYSTEMS ENGINEERING • 2026")
        body_inner = f"""
        <div class="cover-wrapper">
          <div class="cover-top-badge">
            <span class="category-pill">{category}</span>
            <span class="sep">•</span>
            <span class="ilf-brand-tag">ilf-studio.com</span>
          </div>

          <div class="cover-center-content">
            <h1 class="cover-headline">{format_accents(title, theme)}</h1>
            {f'<div class="cover-subtitle-card"><p>{format_accents(subtitle or content, theme)}</p></div>' if (subtitle or content) else ''}
          </div>

          <div class="cover-footer-bar">
            <div class="author-block">
              {f'<img class="author-avatar" src="{avatar_uri}">' if avatar_uri else ''}
              <div class="author-info">
                <div class="author-name">{author_name}</div>
                <div class="author-handle">{author_title}</div>
              </div>
            </div>
            <div class="cover-swipe-pill">Swipe to read →</div>
          </div>
        </div>
        """
        return f'<div class="slide-container slide-page slide-cover theme-{theme}">{body_inner}</div>'

    # ARCHETYPE 2: KPI / BIG NUMBER CALLOUT
    elif stype == "kpi":
        metric = slide_data.get("metric", "10x")
        metric_label = slide_data.get("metric_label", "IMPROVEMENT")
        metric_status = slide_data.get("metric_status", "PROVEN")
        bullets = slide_data.get("bullets", [])
        bullets_html = "".join([f'<li><span class="bullet-check">✓</span><span>{format_accents(b, theme)}</span></li>' for b in bullets])

        body_inner = f"""
        {header_html}
        <div class="slide-body">
          <h2 class="slide-title">{format_accents(title, theme)}</h2>
          {f'<div class="slide-subtitle">{subtitle}</div>' if subtitle else ''}

          <div class="kpi-hero-card">
            <div class="kpi-metric-row">
              <span class="kpi-number">{metric}</span>
              <span class="kpi-status-badge">{metric_status}</span>
            </div>
            <div class="kpi-label">{metric_label}</div>
          </div>

          {f'<div class="kpi-bullets-card"><ul>{bullets_html}</ul></div>' if bullets else ''}
          {f'<div class="editorial-card"><p>{format_accents(content, theme)}</p></div>' if content else ''}
        </div>
        {footer_html}
        """

    # ARCHETYPE 3: DONUT CHART DATA VISUALIZATION (Pure SVG)
    elif stype in ("donut", "donut_chart"):
        segments = slide_data.get("segments", [
            {"label": "Routine Boilerplate", "val": 65, "color": "#CC7A3E", "desc": "Repetitive CRUD, setup, config"},
            {"label": "Integration Plumbing", "val": 25, "color": "#E5A97D", "desc": "APIs, auth tokens, glue code"},
            {"label": "Core Innovation", "val": 10, "color": "#34D399", "desc": "Proprietary business logic & moat"}
        ])
        center_metric = slide_data.get("center_metric", "90%")
        center_label = slide_data.get("center_label", "COMMODITIZED")
        takeaway = slide_data.get("takeaway", content or "Systems engineering is the only defensible advantage remaining.")
        donut_svg = generate_svg_donut(segments, size=380, stroke_width=44)

        legend_items = ""
        for seg in segments:
            lbl = seg.get("label", "")
            val = seg.get("val", 0)
            col = seg.get("color", "var(--accent)")
            desc = seg.get("desc", "")
            legend_items += f"""
            <div class="donut-legend-card">
              <div class="legend-dot" style="background: {col};"></div>
              <div class="legend-content">
                <div class="legend-top-row">
                  <span class="legend-name">{lbl}</span>
                  <span class="legend-val" style="color: {col};">{val}%</span>
                </div>
                {f'<div class="legend-desc">{desc}</div>' if desc else ''}
                <div class="legend-mini-bar"><div class="mini-bar-fill" style="width: {val}%; background: {col};"></div></div>
              </div>
            </div>
            """

        body_inner = f"""
        {header_html}
        <div class="slide-body">
          <h2 class="slide-title">{format_accents(title, theme)}</h2>
          {f'<div class="slide-subtitle">{subtitle}</div>' if subtitle else ''}

          <div class="donut-visual-container">
            <div class="donut-graphic-hub">
              {donut_svg}
              <div class="donut-center-content">
                <div class="donut-center-metric">{center_metric}</div>
                <div class="donut-center-label">{center_label}</div>
              </div>
            </div>
            <div class="donut-legend-column">
              {legend_items}
            </div>
          </div>

          <div class="visual-takeaway-bar">
            <span class="takeaway-tag">VERDICT</span>
            <p>{format_accents(takeaway, theme)}</p>
          </div>
        </div>
        {footer_html}
        """

    # ARCHETYPE 4: METRIC COMPARISON BARS (Progress Meters & Speedups)
    elif stype in ("metric_bars", "bars"):
        bars = slide_data.get("bars", [
            {"label": "Manual Agency Workflow", "value": "40 hrs/mo", "percent": 95, "color": "var(--danger)", "badge": "LEGACY"},
            {"label": "Low-Code Zapier / Make", "value": "12 hrs/mo", "percent": 50, "color": "rgba(250,245,235,0.4)", "badge": "FRAGILE"},
            {"label": "Autonomous Docker Stack", "value": "18 mins/mo", "percent": 10, "color": "var(--emerald)", "badge": "40x SPEEDUP"}
        ])
        delta_stat = slide_data.get("delta_stat", "-98%")
        delta_label = slide_data.get("delta_label", "CYCLE TIME REDUCTION")
        takeaway = slide_data.get("takeaway", content or "Deterministic code running 24/7 on Hetzner VPS beats fragile drag-and-drop triggers.")

        bars_markup = ""
        for b in bars:
            b_label = b.get("label", "")
            b_val = b.get("value", "")
            b_pct = b.get("percent", 50)
            b_col = b.get("color", "var(--accent)")
            b_badge = b.get("badge", "")
            bars_markup += f"""
            <div class="metric-bar-item">
              <div class="metric-bar-header">
                <span class="bar-title">{b_label}</span>
                <div class="bar-val-badge">
                  <span class="bar-val">{b_val}</span>
                  {f'<span class="bar-chip" style="border-color: {b_col}; color: {b_col};">{b_badge}</span>' if b_badge else ''}
                </div>
              </div>
              <div class="metric-track">
                <div class="metric-fill" style="width: {b_pct}%; background: {b_col};"></div>
              </div>
            </div>
            """

        body_inner = f"""
        {header_html}
        <div class="slide-body">
          <h2 class="slide-title">{format_accents(title, theme)}</h2>
          {f'<div class="slide-subtitle">{subtitle}</div>' if subtitle else ''}

          <div class="metric-bars-card">
            {bars_markup}
          </div>

          <div class="metric-delta-highlight-card">
            <div class="delta-number">{delta_stat}</div>
            <div class="delta-meta">
              <div class="delta-title">{delta_label}</div>
              <div class="delta-desc">{format_accents(takeaway, theme)}</div>
            </div>
          </div>
        </div>
        {footer_html}
        """

    # ARCHETYPE 5: ECOSYSTEM / INTEGRATION PIPELINE (Prominent 72px Brand Nodes)
    elif stype in ("ecosystem", "integration"):
        nodes = slide_data.get("nodes", [
            {"brand": "figma", "name": "Figma Tokens", "role": "UI & Design Specs", "arrow_label": "Webhook JSON"},
            {"brand": "claude", "name": "Claude 3.5 Sonnet", "role": "AST Code Generation", "arrow_label": "Structured Diff"},
            {"brand": "n8n", "name": "n8n Engine", "role": "Stateful Orchestration", "arrow_label": "Docker API"},
            {"brand": "postgresql", "name": "PostgreSQL Ledger", "role": "ACID State & Audit", "arrow_label": "Committed"}
        ])
        takeaway = slide_data.get("takeaway", content or "Each layer operates with a strict contract, eliminating runtime surprises.")

        nodes_html = ""
        for i, nd in enumerate(nodes):
            brand = nd.get("brand", "")
            brand_svg = load_svg_logo(brand)
            nd_name = nd.get("name", brand.title())
            nd_role = nd.get("role", "")
            arrow_lbl = nd.get("arrow_label", "")

            arrow_markup = ""
            if i < len(nodes) - 1:
                arrow_markup = f"""
                <div class="ecosystem-connector-row">
                  <div class="connector-v-line"></div>
                  {f'<span class="connector-protocol-pill">{arrow_lbl}</span>' if arrow_lbl else '<span class="connector-arrow-down">↓</span>'}
                  <div class="connector-v-line"></div>
                </div>
                """

            nodes_html += f"""
            <div class="ecosystem-node-item">
              <div class="ecosystem-node-card">
                <div class="ecosystem-brand-circle">
                  {brand_svg or f'<span class="brand-fallback-char">{brand[:2].upper()}</span>'}
                </div>
                <div class="ecosystem-node-meta">
                  <div class="ecosystem-node-name">{nd_name}</div>
                  <div class="ecosystem-node-role">{nd_role}</div>
                </div>
                <div class="ecosystem-node-step">{i+1:02d}</div>
              </div>
              {arrow_markup}
            </div>
            """

        body_inner = f"""
        {header_html}
        <div class="slide-body">
          <h2 class="slide-title">{format_accents(title, theme)}</h2>
          {f'<div class="slide-subtitle">{subtitle}</div>' if subtitle else ''}

          <div class="ecosystem-canvas">
            {nodes_html}
          </div>

          <div class="visual-takeaway-bar">
            <span class="takeaway-tag">ARCHITECTURE</span>
            <p>{format_accents(takeaway, theme)}</p>
          </div>
        </div>
        {footer_html}
        """

    # ARCHETYPE 6: PYRAMID MENTAL MODEL (McKinsey / Minto 3-Tier Hierarchy)
    elif stype in ("pyramid", "hierarchy"):
        tiers = slide_data.get("tiers", [
            {"name": "Client Outcomes & Strategic Moat", "desc": "Proprietary interfaces, autonomous dashboards, high retention", "color": "#CC7A3E"},
            {"name": "Deterministic Automation & Agents", "desc": "n8n workflows, self-healing fallbacks, stateful databases", "color": "var(--card-bg)"},
            {"name": "Foundation APIs & Infrastructure", "desc": "Hetzner VPS, Docker, PostgreSQL, LLM endpoints", "color": "var(--bg-surface)"}
        ])
        takeaway = slide_data.get("takeaway", content or "Never build from the bottom up without locking in the top tier outcome.")

        tiers_html = ""
        widths = [62, 82, 100]
        for i, tr in enumerate(tiers):
            t_num = f"{i+1:02d}"
            t_name = tr.get("name", "")
            t_desc = tr.get("desc", "")
            t_w = widths[i] if i < len(widths) else 100
            t_col = tr.get("color", "var(--bg-card)")

            tiers_html += f"""
            <div class="pyramid-tier-container" style="width: {t_w}%;">
              <div class="pyramid-tier-card" style="border-top-color: {t_col};">
                <div class="tier-pill">{t_num}</div>
                <div class="tier-body">
                  <div class="tier-title">{t_name}</div>
                  <div class="tier-desc">{t_desc}</div>
                </div>
              </div>
            </div>
            """

        body_inner = f"""
        {header_html}
        <div class="slide-body">
          <h2 class="slide-title">{format_accents(title, theme)}</h2>
          {f'<div class="slide-subtitle">{subtitle}</div>' if subtitle else ''}

          <div class="pyramid-wrapper">
            {tiers_html}
          </div>

          <div class="visual-takeaway-bar">
            <span class="takeaway-tag">HIERARCHY</span>
            <p>{format_accents(takeaway, theme)}</p>
          </div>
        </div>
        {footer_html}
        """

    # ARCHETYPE 7: VISUAL HERO / EDITORIAL AI ILLUSTRATION SPLIT
    elif stype in ("visual_hero", "photo_hero", "hero_visual"):
        img_path = slide_data.get("image_path", "")
        img_uri = image_to_data_uri(img_path) if img_path else ""
        hero_badge = slide_data.get("hero_badge", "ILF STUDIO • VISUAL")
        hero_metric = slide_data.get("hero_metric", "")
        bullets = slide_data.get("bullets", [])
        bullets_html = "".join([f'<li><span class="bullet-check">✓</span><span>{format_accents(b, theme)}</span></li>' for b in bullets])
        caption = slide_data.get("caption", "")
        takeaway = slide_data.get("takeaway", content or "")

        hero_framed = "hero-media-framed" if slide_data.get("framed", False) else ""
        hero_full = "hero-media-full" if not bullets and not takeaway and not caption else ""

        body_inner = f"""
        {header_html}
        <div class="slide-body slide-body-hero">
          <h2 class="slide-title">{format_accents(title, theme)}</h2>
          {f'<div class="slide-subtitle">{subtitle}</div>' if subtitle else ''}

          <div class="hero-media-wrapper {hero_full} {hero_framed}">
            {f'<img class="hero-media-image" src="{img_uri}">' if img_uri else '<div class="hero-media-placeholder">Visual Platform Canvas</div>'}
            {f'<div class="hero-overlay-pill">{hero_badge}</div>' if hero_badge else ''}
            {f'<div class="hero-metric-overlay">{hero_metric}</div>' if hero_metric else ''}
          </div>

          {f'<div class="hero-caption-card"><p>{format_accents(caption, theme)}</p></div>' if caption else ''}
          {f'<div class="hero-bullets-card"><ul>{bullets_html}</ul></div>' if bullets else ''}
          {f'<div class="visual-takeaway-bar"><span class="takeaway-tag">SYSTEM</span><p>{format_accents(takeaway, theme)}</p></div>' if takeaway else ''}
        </div>
        {footer_html}
        """

    # ARCHETYPE 8: BENTO COMPARISON (BEFORE vs AFTER / LEGACY vs AI-NATIVE)
    elif stype == "comparison":
        left = slide_data.get("left") or {
            "title": slide_data.get("legacy_title", "The Legacy Way"),
            "items": slide_data.get("legacy_items", [])
        }
        right = slide_data.get("right") or {
            "title": slide_data.get("native_title", "The AI-Native Stack"),
            "items": slide_data.get("native_items", [])
        }
        left_items = "".join([f'<li><span class="cross-icon">✕</span><span>{item}</span></li>' for item in left.get("items", [])])
        right_items = "".join([f'<li><span class="check-icon">✓</span><span>{item}</span></li>' for item in right.get("items", [])])

        body_inner = f"""
        {header_html}
        <div class="slide-body">
          <h2 class="slide-title">{format_accents(title, theme)}</h2>
          {f'<div class="slide-subtitle">{subtitle}</div>' if subtitle else ''}

          <div class="bento-comparison-grid">
            <div class="bento-column legacy-column">
              <div class="column-header">
                <span class="column-badge badge-legacy">LEGACY</span>
                <h3 class="column-title">{left.get("title", "Legacy")}</h3>
              </div>
              <ul class="column-list">{left_items}</ul>
            </div>

            <div class="bento-column modern-column">
              <div class="column-header">
                <span class="column-badge badge-modern">AI-NATIVE</span>
                <h3 class="column-title">{right.get("title", "AI-Native")}</h3>
              </div>
              <ul class="column-list">{right_items}</ul>
            </div>
          </div>

          {f'<div class="editorial-card conclusion-card"><p><strong>Verdict:</strong> {format_accents(slide_data.get("takeaway", content or ""), theme)}</p></div>' if slide_data.get("takeaway") or content else ''}
        </div>
        {footer_html}
        """

    # ARCHETYPE 9: PIPELINE / STEPPER FLOW
    elif stype == "pipeline":
        steps = slide_data.get("steps", [])
        steps_html = ""
        for i, st in enumerate(steps):
            num = f"{i+1:02d}"
            st_title = st.get("title", f"Phase {i+1}")
            st_desc = st.get("desc", "")
            st_badge = st.get("badge", "")
            steps_html += f"""
            <div class="pipeline-step-card">
              <div class="step-num-pill">{num}</div>
              <div class="step-content">
                <div class="step-header-row">
                  <span class="step-name">{st_title}</span>
                  {f'<span class="step-badge">{st_badge}</span>' if st_badge else ''}
                </div>
                <div class="step-desc">{format_accents(st_desc, theme)}</div>
              </div>
            </div>
            """

        body_inner = f"""
        {header_html}
        <div class="slide-body">
          <h2 class="slide-title">{format_accents(title, theme)}</h2>
          {f'<div class="slide-subtitle">{subtitle}</div>' if subtitle else ''}
          <div class="pipeline-flow-container">
            {steps_html}
          </div>
          {f'<div class="pipeline-takeaway-card"><strong>Core rule:</strong> {format_accents(content, theme)}</div>' if content else ''}
        </div>
        {footer_html}
        """

    # ARCHETYPE 10: 2x2 QUADRANT / MATRIX
    elif stype == "quadrant":
        quadrants = slide_data.get("quadrants", [])
        q_html = ""
        for i, q in enumerate(quadrants):
            q_title = q.get("title", "")
            q_desc = q.get("desc", "")
            q_badge = q.get("badge", f"Q{i+1}")
            q_html += f"""
            <div class="quadrant-cell q-cell-{i+1}">
              <div class="q-cell-header">
                <span class="q-badge">{q_badge}</span>
                <span class="q-title">{q_title}</span>
              </div>
              <p class="q-desc">{format_accents(q_desc, theme)}</p>
            </div>
            """

        body_inner = f"""
        {header_html}
        <div class="slide-body">
          <h2 class="slide-title">{format_accents(title, theme)}</h2>
          {f'<div class="slide-subtitle">{subtitle}</div>' if subtitle else ''}
          <div class="quadrant-grid">
            {q_html}
          </div>
          {f'<div class="editorial-card"><p>{format_accents(content, theme)}</p></div>' if content else ''}
        </div>
        {footer_html}
        """

    # ARCHETYPE 11: SUMMARY / CTA (Fixed non-wrapping save button!)
    elif stype == "cta":
        takeaways = slide_data.get("takeaways") or slide_data.get("items", [])
        takeaways_html = "".join([f'<li><span class="bullet-num">{i+1:02d}</span><span>{format_accents(t, theme)}</span></li>' for i, t in enumerate(takeaways)])
        cta_text = slide_data.get("cta_text", "Save this post for your engineering team")

        body_inner = f"""
        {header_html}
        <div class="slide-body">
          <h2 class="slide-title">{format_accents(title or "Key Takeaways", theme)}</h2>

          {f'<div class="cta-takeaways-card"><ul class="takeaways-list">{takeaways_html}</ul></div>' if takeaways else ''}

          <div class="cta-author-hero-card">
            {f'<img class="cta-hero-avatar" src="{avatar_uri}">' if avatar_uri else ''}
            <div class="cta-hero-info">
              <div class="cta-hero-name">{author_name}</div>
              <div class="cta-hero-handle">@ilovefiniki • ilf-studio.com</div>
              <p class="cta-hero-desc">{author_title}</p>
            </div>
          </div>

          <div class="cta-action-box">
            <span class="cta-action-icon">🔖</span>
            <div class="cta-action-text">{format_accents(cta_text, theme)}</div>
          </div>
        </div>
        {footer_html}
        """

    # DEFAULT ARCHETYPE: EDITORIAL / DEEP DIVE
    else:
        bullets = slide_data.get("bullets", [])
        bullets_html = ""
        if bullets:
            b_items = "".join([f'<li><span class="bullet-dot"></span><span>{format_accents(b, theme)}</span></li>' for b in bullets])
            bullets_html = f'<ul class="editorial-bullets">{b_items}</ul>'

        body_inner = f"""
        {header_html}
        <div class="slide-body">
          <h2 class="slide-title">{format_accents(title, theme)}</h2>
          {f'<div class="slide-lead">{format_accents(subtitle, theme)}</div>' if subtitle else ''}
          <div class="editorial-card">
            <p>{format_accents(content, theme)}</p>
          </div>
          {bullets_html}
        </div>
        {footer_html}
        """

    return f'<div class="slide-container slide-page theme-{theme}">{body_inner}</div>'


def generate_full_html(slides: list[dict], theme: str = "dark", author_data: dict = None) -> str:
    slides_markup = "\n".join([
        build_slide_html(s, i + 1, len(slides), theme, author_data)
        for i, s in enumerate(slides)
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Geist:wght@400;500;600;700;800&display=swap');

  @page {{
    size: 1080px 1350px;
    margin: 0;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  body {{
    margin: 0;
    padding: 0;
    background: #000000;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  }}

  /* THEME TOKENS */
  .theme-dark {{
    --bg-main: #12100E;
    --bg-surface: #181512;
    --bg-card: #1C1916;
    --border-card: #2D261E;
    --border-subtle: #241E18;
    --text-primary: #FAF5EB;
    --text-secondary: #D4CBBF;
    --text-muted: #8E8477;
    --accent: #CC7A3E;
    --accent-soft: rgba(204, 122, 62, 0.12);
    --emerald: #34D399;
    --emerald-soft: rgba(52, 211, 153, 0.12);
    --danger: #F87171;
    --danger-soft: rgba(248, 113, 113, 0.12);
  }}

  .theme-paper {{
    --bg-main: #EFE8DC;
    --bg-surface: #E8DFD1;
    --bg-card: #FFFFFF;
    --border-card: #D8CEBE;
    --border-subtle: #DECDBB;
    --text-primary: #1B1917;
    --text-secondary: #44403C;
    --text-muted: #78716C;
    --accent: #C2531A;
    --accent-soft: rgba(194, 83, 26, 0.1);
    --emerald: #059669;
    --emerald-soft: rgba(5, 150, 105, 0.1);
    --danger: #DC2626;
    --danger-soft: rgba(220, 38, 38, 0.1);
  }}

  /* Crisp, clean borders on paper theme (kills dirty drop-shadows) */
  .theme-paper .ecosystem-node-card,
  .theme-paper .donut-visual-container,
  .theme-paper .metric-bars-card,
  .theme-paper .pyramid-tier-card,
  .theme-paper .editorial-card,
  .theme-paper .hero-media-wrapper.hero-media-framed,
  .theme-paper .bento-column,
  .theme-paper .pipeline-step-card,
  .theme-paper .quadrant-cell,
  .theme-paper .cta-takeaways-card,
  .theme-paper .cta-author-hero-card,
  .theme-paper .cover-subtitle-card,
  .theme-paper .kpi-hero-card {{
    box-shadow: none !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
  }}

  .theme-paper .hero-media-wrapper {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
  }}

  .theme-paper .ecosystem-brand-circle {{
    background: #F5EFE6 !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
  }}

  .slide-container {{
    width: 1080px;
    height: 1350px;
    position: relative;
    overflow: hidden;
    background: var(--bg-main);
    color: var(--text-primary);
    padding: 72px 76px 64px 76px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    page-break-after: always;
  }}

  /* HEADER */
  .slide-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 48px;
    margin-bottom: 24px;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 18px;
  }}

  .header-left {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .badge-pill {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--accent);
    background: var(--accent-soft);
    padding: 6px 14px;
    border-radius: 999px;
    border: 1px solid rgba(204, 122, 62, 0.25);
  }}

  .brand-bar {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .brand-chip {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 12px;
    color: var(--text-secondary);
  }}

  .brand-chip svg {{
    width: 16px;
    height: 16px;
  }}

  .slide-counter {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-muted);
  }}

  /* BODY */
  .slide-body {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 20px;
  }}

  .slide-title {{
    font-size: 46px;
    font-weight: 800;
    line-height: 1.18;
    letter-spacing: -0.03em;
    color: var(--text-primary);
  }}

  .slide-subtitle {{
    font-size: 21px;
    line-height: 1.45;
    color: var(--text-secondary);
  }}

  .editorial-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 20px;
    padding: 28px 34px;
    font-size: 22px;
    line-height: 1.55;
    color: var(--text-secondary);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25);
  }}

  .inline-code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9em;
    background: rgba(255, 255, 255, 0.08);
    color: var(--accent);
    padding: 3px 8px;
    border-radius: 6px;
  }}

  /* KPI STYLES */
  .kpi-hero-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-left: 6px solid var(--accent);
    border-radius: 24px;
    padding: 40px 48px;
  }}

  .kpi-metric-row {{
    display: flex;
    align-items: baseline;
    gap: 20px;
  }}

  .kpi-number {{
    font-size: 110px;
    font-weight: 900;
    letter-spacing: -0.05em;
    color: var(--text-primary);
    line-height: 1;
  }}

  .kpi-status-badge {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 16px;
    font-weight: 700;
    background: var(--emerald-soft);
    color: var(--emerald);
    padding: 8px 18px;
    border-radius: 999px;
  }}

  .kpi-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: var(--accent);
    margin-top: 10px;
  }}

  .kpi-bullets-card ul {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}

  .kpi-bullets-card li {{
    display: flex;
    align-items: flex-start;
    gap: 14px;
    font-size: 20px;
    color: var(--text-secondary);
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 14px;
    padding: 16px 20px;
  }}

  .bullet-check {{
    color: var(--emerald);
    font-weight: 900;
  }}

  /* DONUT CHART VISUAL STYLES */
  .donut-visual-container {{
    display: flex;
    align-items: center;
    gap: 36px;
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 24px;
    padding: 32px 36px;
  }}

  .donut-graphic-hub {{
    position: relative;
    width: 380px;
    height: 380px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .donut-center-content {{
    position: absolute;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }}

  .donut-center-metric {{
    font-size: 58px;
    font-weight: 900;
    letter-spacing: -0.04em;
    color: var(--text-primary);
    line-height: 1;
  }}

  .donut-center-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--accent);
    margin-top: 6px;
  }}

  .donut-legend-column {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}

  .donut-legend-card {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 14px 18px;
  }}

  .legend-dot {{
    width: 14px;
    height: 14px;
    border-radius: 4px;
    margin-top: 4px;
    flex-shrink: 0;
  }}

  .legend-content {{
    flex: 1;
  }}

  .legend-top-row {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
  }}

  .legend-val {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 18px;
  }}

  .legend-desc {{
    font-size: 14px;
    color: var(--text-muted);
    margin: 4px 0 8px 0;
  }}

  .legend-mini-bar {{
    height: 6px;
    width: 100%;
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    overflow: hidden;
  }}

  .mini-bar-fill {{
    height: 100%;
    border-radius: 999px;
  }}

  /* METRIC BARS COMPARISON STYLES */
  .metric-bars-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 24px;
    padding: 32px 36px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }}

  .metric-bar-item {{
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  .metric-bar-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }}

  .bar-title {{
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
  }}

  .bar-val-badge {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .bar-val {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
  }}

  .bar-chip {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    border: 1px solid;
    padding: 3px 8px;
    border-radius: 6px;
  }}

  .metric-track {{
    height: 16px;
    width: 100%;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 999px;
    overflow: hidden;
  }}

  .metric-fill {{
    height: 100%;
    border-radius: 999px;
    box-shadow: 0 0 12px rgba(204, 122, 62, 0.3);
  }}

  .metric-delta-highlight-card {{
    display: flex;
    align-items: center;
    gap: 24px;
    background: var(--accent-soft);
    border: 1px solid rgba(204, 122, 62, 0.3);
    border-radius: 20px;
    padding: 24px 32px;
  }}

  .delta-number {{
    font-size: 64px;
    font-weight: 900;
    color: var(--accent);
    line-height: 1;
    font-family: 'Plus Jakarta Sans', sans-serif;
  }}

  .delta-meta {{
    flex: 1;
  }}

  .delta-title {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--accent);
  }}

  .delta-desc {{
    font-size: 18px;
    color: var(--text-secondary);
    margin-top: 4px;
  }}

  /* ECOSYSTEM INTEGRATION PIPELINE (Large 72px Brand Logos) */
  .ecosystem-canvas {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .ecosystem-node-item {{
    display: flex;
    flex-direction: column;
    align-items: center;
  }}

  .ecosystem-node-card {{
    width: 100%;
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 20px;
    padding: 18px 28px;
    display: flex;
    align-items: center;
    gap: 24px;
    position: relative;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  }}

  .ecosystem-brand-circle {{
    width: 68px;
    height: 68px;
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.04);
    border: 2px solid var(--border-card);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}

  .ecosystem-brand-circle svg {{
    width: 38px;
    height: 38px;
  }}

  .brand-fallback-char {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 24px;
    font-weight: 800;
    color: var(--accent);
  }}

  .ecosystem-node-meta {{
    flex: 1;
  }}

  .ecosystem-node-name {{
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
  }}

  .ecosystem-node-role {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--accent);
    margin-top: 2px;
  }}

  .ecosystem-node-step {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    font-weight: 800;
    color: var(--text-muted);
  }}

  .ecosystem-connector-row {{
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 40px;
    justify-content: center;
    position: relative;
  }}

  .connector-v-line {{
    width: 2px;
    height: 10px;
    background: var(--border-card);
  }}

  .connector-protocol-pill {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    background: var(--bg-surface);
    border: 1px solid var(--border-card);
    color: var(--text-muted);
    padding: 2px 10px;
    border-radius: 999px;
  }}

  .connector-arrow-down {{
    font-size: 16px;
    color: var(--accent);
  }}

  /* PYRAMID MENTAL MODEL STYLES */
  .pyramid-wrapper {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    margin: 10px 0;
  }}

  .pyramid-tier-container {{
    transition: all 0.3s ease;
  }}

  .pyramid-tier-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-top: 4px solid var(--accent);
    border-radius: 18px;
    padding: 22px 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  }}

  .tier-pill {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 18px;
    font-weight: 800;
    background: var(--accent-soft);
    color: var(--accent);
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}

  .tier-body {{
    flex: 1;
  }}

  .tier-title {{
    font-size: 20px;
    font-weight: 800;
    color: var(--text-primary);
  }}

  .tier-desc {{
    font-size: 15px;
    color: var(--text-secondary);
    margin-top: 4px;
  }}

  /* VISUAL HERO MEDIA SPLIT */
  .hero-media-wrapper {{
    position: relative;
    width: 100%;
    height: 600px;
    border-radius: 20px;
    overflow: hidden;
    background: transparent;
    border: none;
    box-shadow: none;
    margin-top: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .hero-media-wrapper.hero-media-framed {{
    background: #181513;
    border: 1px solid var(--border-card);
    box-shadow: 0 16px 40px rgba(0,0,0,0.3);
  }}

  .hero-media-wrapper.hero-media-framed .hero-media-image {{
    object-fit: cover;
  }}

  .hero-media-wrapper.hero-media-full {{
    height: 720px;
  }}

  .hero-media-image {{
    width: 100%;
    height: 100%;
    object-fit: contain;
    object-position: center;
    border-radius: 12px;
  }}

  .hero-caption-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 16px;
    padding: 18px 24px;
    font-size: 18px;
    color: var(--text-secondary);
    line-height: 1.5;
    margin-top: 16px;
  }}

  .hero-overlay-pill {{
    position: absolute;
    top: 20px;
    left: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.05em;
    background: var(--accent);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #FFFFFF;
    padding: 6px 14px;
    border-radius: 999px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    backdrop-filter: blur(8px);
    z-index: 2;
  }}

  .hero-metric-overlay {{
    position: absolute;
    bottom: 20px;
    right: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    background: var(--emerald-soft);
    border: 1px solid var(--emerald);
    color: var(--emerald);
    padding: 6px 14px;
    border-radius: 999px;
    backdrop-filter: blur(8px);
  }}

  .hero-bullets-card ul {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}

  .hero-bullets-card li {{
    display: flex;
    align-items: center;
    gap: 14px;
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 14px;
    padding: 16px 22px;
    font-size: 19px;
    color: var(--text-secondary);
  }}

  .visual-takeaway-bar {{
    display: flex;
    align-items: center;
    gap: 16px;
    background: var(--accent-soft);
    border: 1px solid rgba(204, 122, 62, 0.25);
    border-radius: 16px;
    padding: 16px 24px;
  }}

  .takeaway-tag {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 800;
    background: var(--accent);
    color: #FFFFFF;
    padding: 4px 10px;
    border-radius: 6px;
    flex-shrink: 0;
  }}

  .visual-takeaway-bar p {{
    font-size: 17px;
    color: var(--text-primary);
  }}

  /* BENTO COMPARISON */
  .bento-comparison-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }}

  .bento-column {{
    border-radius: 20px;
    padding: 28px 24px;
  }}

  .legacy-column {{
    background: var(--danger-soft);
    border: 1px solid rgba(248, 113, 113, 0.2);
  }}

  .modern-column {{
    background: var(--emerald-soft);
    border: 1px solid rgba(52, 211, 153, 0.2);
  }}

  .column-header {{
    margin-bottom: 20px;
  }}

  .column-badge {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 999px;
  }}

  .badge-legacy {{
    background: rgba(248, 113, 113, 0.2);
    color: var(--danger);
  }}

  .badge-modern {{
    background: rgba(52, 211, 153, 0.2);
    color: var(--emerald);
  }}

  .column-title {{
    font-size: 22px;
    font-weight: 800;
    margin-top: 10px;
    color: var(--text-primary);
  }}

  .column-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}

  .column-list li {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    font-size: 17px;
    line-height: 1.45;
    color: var(--text-secondary);
  }}

  .cross-icon {{
    color: var(--danger);
    font-weight: 900;
  }}

  .check-icon {{
    color: var(--emerald);
    font-weight: 900;
  }}

  /* PIPELINE */
  .pipeline-flow-container {{
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}

  .pipeline-step-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 16px;
    padding: 18px 24px;
    display: flex;
    align-items: center;
    gap: 20px;
  }}

  .step-num-pill {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 16px;
    font-weight: 700;
    background: var(--accent-soft);
    color: var(--accent);
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}

  .step-content {{
    flex: 1;
  }}

  .step-header-row {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .step-name {{
    font-size: 19px;
    font-weight: 700;
    color: var(--text-primary);
  }}

  .step-badge {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    background: rgba(255, 255, 255, 0.08);
    color: var(--text-muted);
    padding: 2px 8px;
    border-radius: 4px;
  }}

  .step-desc {{
    font-size: 15px;
    color: var(--text-secondary);
    margin-top: 4px;
  }}

  /* 2X2 QUADRANTS */
  .quadrant-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }}

  .quadrant-cell {{
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 18px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  .q-cell-header {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  .q-badge {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    background: var(--accent-soft);
    color: var(--accent);
    padding: 4px 8px;
    border-radius: 6px;
  }}

  .q-title {{
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
  }}

  .q-desc {{
    font-size: 15px;
    color: var(--text-secondary);
    line-height: 1.45;
  }}

  /* CTA STYLING (FIXED BUTTON WRAP) */
  .cta-takeaways-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 20px;
    padding: 24px 30px;
  }}

  .takeaways-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}

  .takeaways-list li {{
    display: flex;
    align-items: flex-start;
    gap: 14px;
    font-size: 19px;
    color: var(--text-secondary);
  }}

  .bullet-num {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    font-weight: 700;
    color: var(--accent);
    background: var(--accent-soft);
    padding: 3px 8px;
    border-radius: 6px;
    flex-shrink: 0;
  }}

  .cta-author-hero-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border-card);
    border-radius: 20px;
    padding: 24px 30px;
    display: flex;
    align-items: center;
    gap: 20px;
  }}

  .cta-hero-avatar {{
    width: 72px;
    height: 72px;
    border-radius: 22px;
    object-fit: cover;
    border: 2px solid var(--accent);
    flex-shrink: 0;
  }}

  .cta-hero-info {{
    flex: 1;
  }}

  .cta-hero-name {{
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
  }}

  .cta-hero-handle {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--accent);
    margin-top: 2px;
  }}

  .cta-hero-desc {{
    font-size: 15px;
    color: var(--text-muted);
    margin-top: 4px;
  }}

  .cta-action-box {{
    display: flex;
    align-items: center;
    gap: 20px;
    background: var(--accent-soft);
    border: 1px solid rgba(204, 122, 62, 0.3);
    border-radius: 20px;
    padding: 24px 32px;
  }}

  .cta-action-icon {{
    font-size: 28px;
    flex-shrink: 0;
  }}

  .cta-action-text {{
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.4;
  }}

  /* COVER STYLING */
  .slide-cover {{
    justify-content: space-between;
    padding: 88px 84px 80px 84px;
  }}

  .cover-wrapper {{
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .cover-center-content {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    flex: 1;
    margin: 40px 0;
  }}

  .cover-top-badge {{
    display: inline-flex;
    align-items: center;
    gap: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
  }}

  .category-pill {{
    color: var(--accent);
    background: var(--accent-soft);
    padding: 6px 14px;
    border-radius: 999px;
  }}

  .ilf-brand-tag {{
    color: var(--text-muted);
  }}

  .sep {{
    color: var(--text-muted);
  }}

  .cover-headline {{
    font-size: 68px;
    font-weight: 800;
    line-height: 1.14;
    letter-spacing: -0.04em;
    color: var(--text-primary);
    margin: 0 0 32px 0;
  }}

  .cover-subtitle-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-left: 6px solid var(--accent);
    border-radius: 20px;
    padding: 34px 42px;
  }}

  .cover-subtitle-card p {{
    font-size: 25px;
    line-height: 1.45;
    color: var(--text-secondary);
  }}

  .cover-footer-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 32px;
    border-top: 1px solid var(--border-subtle);
  }}

  .author-block {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .author-avatar {{
    width: 56px;
    height: 56px;
    border-radius: 18px;
    object-fit: cover;
    border: 2px solid var(--accent);
  }}

  .author-name {{
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
  }}

  .author-handle {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--text-muted);
  }}

  .cover-swipe-pill {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 15px;
    font-weight: 700;
    background: var(--accent);
    color: #FFFFFF;
    padding: 10px 22px;
    border-radius: 999px;
  }}

  /* FOOTER */
  .slide-footer {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 48px;
    margin-top: 24px;
    padding-top: 18px;
    border-top: 1px solid var(--border-subtle);
  }}

  .footer-author {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .footer-avatar {{
    width: 38px;
    height: 38px;
    border-radius: 12px;
    object-fit: cover;
  }}

  .footer-meta {{
    display: flex;
    flex-direction: column;
  }}

  .footer-name {{
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
  }}

  .footer-title {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--text-muted);
  }}

  .swipe-indicator {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    font-weight: 600;
    color: var(--accent);
  }}
</style>
</head>
<body>
  {slides_markup}
</body>
</html>
"""


def auto_infer_slide_type(text: str) -> dict:
    """Intelligently detects the best visual archetype if a slide is just text."""
    lower = text.lower()

    # Check for KPI / Big Numbers
    if re.search(r"\b(\d+%\b|\d+x\b|€\d+|\$\d+|\b\d+\s*(hours|hrs|days|mins))", text, re.IGNORECASE):
        m = re.search(r"(\d+[%xX]|\b\d+\s*(?:hours|hrs|days|mins))", text, re.IGNORECASE)
        metric_str = m.group(1) if m else "10x"
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        title = lines[0] if lines else "Key Metric"
        bullets = [l.lstrip("-•* ") for l in lines[1:] if l.startswith(("-", "•", "*"))]
        content = " ".join([l for l in lines[1:] if not l.startswith(("-", "•", "*"))])
        return {
            "archetype": "kpi",
            "title": title,
            "metric": metric_str,
            "metric_label": "MEASURED IMPACT",
            "bullets": bullets[:3],
            "content": content
        }

    # Check for Comparison
    if " vs " in lower or "versus" in lower or "instead of" in lower:
        return {
            "archetype": "comparison",
            "title": "Legacy Approach vs The AI-Native Way",
            "left": {"title": "Legacy Manual Way", "items": ["Fragmented tools with no state", "Brittle webhook triggers", "Manual error debugging"]},
            "right": {"title": "Autonomous Engine", "items": ["ACID PostgreSQL ledger", "Self-healing error fallback", "Zero latency execution"]},
            "content": text
        }

    # Default Editorial
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    title = lines[0] if lines else "System Strategy"
    bullets = [l.lstrip("-•* ") for l in lines[1:] if l.startswith(("-", "•", "*"))]
    content = " ".join([l for l in lines[1:] if not l.startswith(("-", "•", "*"))])
    return {
        "archetype": "editorial",
        "title": title,
        "bullets": bullets,
        "content": content
    }


def render_carousel_pdf(slides: list[dict], output_pdf: str, theme: str = "dark", author_data: dict = None, save_pngs: bool = True):
    """Compiles slides into vector PDF (1080x1350) and generates 2x Retina PNGs."""
    html_content = generate_full_html(slides, theme=theme, author_data=author_data)

    out_path = Path(output_pdf)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use 1080x1350 viewport with device_scale_factor=2 for crisp Retina snapshots
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        page.set_content(html_content, wait_until="networkidle")

        # 1. Print full vector PDF
        page.pdf(
            path=str(out_path),
            width="1080px",
            height="1350px",
            print_background=True,
            margin={"top": "0px", "right": "0px", "bottom": "0px", "left": "0px"}
        )
        print(f"✓ Vector PDF rendered: {out_path} ({len(slides)} slides)")

        # 2. Render individual Retina PNGs if requested
        if save_pngs:
            preview_dir = out_path.parent / f"previews_{out_path.stem}"
            preview_dir.mkdir(parents=True, exist_ok=True)
            slide_elements = page.query_selector_all(".slide-page")
            for i, elem in enumerate(slide_elements):
                png_path = preview_dir / f"slide_{i+1:02d}.png"
                elem.screenshot(path=str(png_path))
            print(f"✓ PNG previews saved to: {preview_dir}")

        browser.close()

    # Watermarks remover cleanup if available
    if clean_file_path:
        try:
            clean_file_path(str(out_path))
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="LinkedIn Carousel Generator v2.1")
    parser.add_argument("--slides-file", help="Path to JSON file containing structured slide objects")
    parser.add_argument("--title", help="Cover slide headline")
    parser.add_argument("--subtitle", help="Cover slide subtitle")
    parser.add_argument("--slides", help="JSON array of slide texts or objects")
    parser.add_argument("--cta", default="Save this post for your engineering team", help="CTA slide text")
    parser.add_argument("--slug", required=True, help="Filename slug")
    parser.add_argument("--output-dir", default="/Users/vit/PROJECTS/Social Media posting/carousels/", help="Output folder")
    parser.add_argument("--avatar", default="/Users/vit/PROJECTS/Shared Skills/.agents/skills/quote_image_creator/assets/avatar.jpg", help="Path to avatar")
    parser.add_argument("--name", default="Vitaliy Alhimovich", help="Author name")
    parser.add_argument("--job-title", default="AI Engineer | ilf-studio.com", help="Author title")
    parser.add_argument("--theme", default="dark", choices=["dark", "paper"], help="Theme: dark or paper")
    parser.add_argument("--both-themes", action="store_true", help="Generate both dark and paper versions")
    parser.add_argument("--no-cta", action="store_true", help="Skip final CTA slide")

    args = parser.parse_args()

    author_data = {
        "avatar": args.avatar,
        "name": args.name,
        "title": args.job_title
    }

    # Load slides
    final_slides = []
    if args.slides_file:
        with open(args.slides_file, "r", encoding="utf-8") as f:
            final_slides = json.load(f)
    elif args.slides:
        raw_slides = json.loads(args.slides)
        # Cover slide
        if args.title:
            final_slides.append({
                "archetype": "cover",
                "title": args.title,
                "subtitle": args.subtitle or ""
            })
        for item in raw_slides:
            if isinstance(item, dict):
                final_slides.append(item)
            else:
                final_slides.append(auto_infer_slide_type(str(item)))
        if not args.no_cta:
            final_slides.append({
                "archetype": "cta",
                "cta_text": args.cta
            })
    else:
        print("Error: Either --slides-file or --slides with --title is required.")
        sys.exit(1)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    themes = ["dark", "paper"] if args.both_themes else [args.theme]
    for th in themes:
        suffix = f"_{th}" if (args.both_themes or args.theme != "dark") else ""
        pdf_name = f"carousel_{args.slug}{suffix}.pdf"
        render_carousel_pdf(final_slides, str(out_dir / pdf_name), theme=th, author_data=author_data, save_pngs=True)


if __name__ == "__main__":
    main()
