#!/usr/bin/env python3
"""
LinkedIn Carousel Generator — finiki brand v2.0
Generates 1080×1350 portrait slides.

Themes:  dark (ilovefiniki.com) | paper (finiki.in) | cream (ilf.studio)
Accent:  Use **phrase** in --title to highlight a phrase in accent color + Fraunces italic.
Output:  carousels/{slug}_{date}/ subfolder

Usage:
  python3 generate_carousel.py \
    --title "I thought I was careful. **A bot still stole my API key.**" \
    --subtitle "A \$6 lesson I won't forget" \
    --eyebrow "AI SECURITY · LESSON LEARNED" \
    --slides '["Slide 2 text", "Slide 3 text"]' \
    --cta "Follow for honest AI engineering lessons" \
    --slug openai-key-stolen \
    --output-dir "/path/to/carousels/" \
    --avatar /path/to/avatar.jpg \
    --theme dark
"""

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Watermark & provenance hygiene
try:
    WM_REMOVER_DIR = Path(__file__).resolve().parent.parent.parent / "watermarks_remover"
    if str(WM_REMOVER_DIR) not in sys.path:
        sys.path.insert(0, str(WM_REMOVER_DIR))
    from clean_helper import clean_text_str, clean_file_path
except ImportError:
    clean_text_str = lambda s: s
    clean_file_path = lambda p, **kw: None

try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False

# ── Brand tokens ─────────────────────────────────────────────────────────────
THEMES = {
    # ilovefiniki.com · dark · ink-deep bg
    "dark": {
        "bg":          (14, 14, 14),
        "text":        (245, 241, 234, 255),   # paper
        "accent":      (240, 138, 95, 255),    # coral-lt
        "muted":       (245, 241, 234, 90),    # paper @ 35%
        "rule":        (245, 241, 234, 20),    # paper @ 8%
        "bracket":     (245, 241, 234, 30),    # corner brackets
        "ring":        (240, 138, 95, 160),
        "eyebrow":     (240, 138, 95, 180),
        "cover_num":   (245, 241, 234, 55),
    },
    # finiki.in · paper · warm light
    "paper": {
        "bg":          (245, 241, 234),
        "text":        (26, 26, 26, 255),      # ink
        "accent":      (217, 87, 47, 255),     # coral
        "muted":       (26, 26, 26, 90),
        "rule":        (26, 26, 26, 20),
        "bracket":     (26, 26, 26, 35),
        "ring":        (217, 87, 47, 160),
        "eyebrow":     (217, 87, 47, 180),
        "cover_num":   (26, 26, 26, 55),
    },
    # ilf.studio · cream · warm editorial
    "cream": {
        "bg":          (239, 232, 220),
        "text":        (42, 36, 27, 255),      # sepia
        "accent":      (204, 122, 62, 255),    # amber
        "muted":       (42, 36, 27, 90),
        "rule":        (42, 36, 27, 20),
        "bracket":     (42, 36, 27, 35),
        "ring":        (204, 122, 62, 160),
        "eyebrow":     (204, 122, 62, 180),
        "cover_num":   (42, 36, 27, 55),
    },
}

W, H = 1080, 1350
PAD = 72

SKILL_DIR = Path(__file__).parent.parent

# ── Font resolution ───────────────────────────────────────────────────────────
FONT_PATHS = {
    "bold": [
        "/Library/Fonts/Geist-Bold.ttf",
        "/Library/Fonts/Geist/Geist-Bold.ttf",
        "/Library/Fonts/Inter-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ],
    "semibold": [
        "/Library/Fonts/Geist-SemiBold.ttf",
        "/Library/Fonts/Inter-SemiBold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ],
    "regular": [
        "/Library/Fonts/Geist-Regular.ttf",
        "/Library/Fonts/Inter-Regular.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ],
    "mono": [
        "/Applications/PhpStorm.app/Contents/jbr/Contents/Home/lib/fonts/JetBrainsMono-Regular.ttf",
        "/Library/Fonts/JetBrainsMono-Regular.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ],
    "editorial": [
        str(SKILL_DIR / "assets" / "FrauncesItalic.ttf"),
        "/Library/Fonts/Fraunces-Italic.ttf",
        # Fallback: use bold (will lose italic but keep accent color)
    ],
}


def find_font(style="bold"):
    for path in FONT_PATHS.get(style, FONT_PATHS["regular"]):
        if Path(path).exists():
            return path
    # Cascade fallbacks
    for fallback in ["bold", "regular"]:
        for path in FONT_PATHS[fallback]:
            if Path(path).exists():
                return path
    raise FileNotFoundError(f"No usable font found for style: {style}")


# ── Styled text parsing ──────────────────────────────────────────────────────

def parse_styled(text):
    """Parse **accent** markers → list of (str, is_accent)."""
    segments = re.split(r'\*\*(.+?)\*\*', text)
    return [(s, i % 2 == 1) for i, s in enumerate(segments) if s]


def wrap_styled(segments, normal_font, accent_font, draw, max_w):
    """Word-wrap styled segments → list of lines, each a list of (word, is_accent)."""
    words = []
    for text, is_acc in segments:
        for w in text.split():
            words.append((w, is_acc))

    lines, current, cur_w = [], [], 0
    sp_w = draw.textbbox((0, 0), " ", font=normal_font)[2]

    for word, is_acc in words:
        f = accent_font if is_acc else normal_font
        w_w = draw.textbbox((0, 0), word, font=f)[2]
        needed = (sp_w if current else 0) + w_w
        if cur_w + needed > max_w and current:
            lines.append(current)
            current, cur_w = [(word, is_acc)], w_w
        else:
            current.append((word, is_acc))
            cur_w += needed

    if current:
        lines.append(current)
    return lines


PUNCTUATION_ATTACH_LEFT = (".", ",", "!", "?", ":", ";", ")", "]", "}", "...", "”", "’")
PUNCTUATION_ATTACH_RIGHT = ("(", "[", "{", "“", "‘")


def measure_line(line_words, normal_font, accent_font, draw):
    sp_w = draw.textbbox((0, 0), " ", font=normal_font)[2]
    total = 0
    for i, (word, is_acc) in enumerate(line_words):
        f = accent_font if is_acc else normal_font
        has_space = i > 0 and (word not in PUNCTUATION_ATTACH_LEFT) and (line_words[i-1][0] not in PUNCTUATION_ATTACH_RIGHT)
        total += (sp_w if has_space else 0) + draw.textbbox((0, 0), word, font=f)[2]
    return total


def draw_styled_line(draw, x, y, line_words, normal_font, accent_font,
                     normal_color, accent_color):
    sp_w = draw.textbbox((0, 0), " ", font=normal_font)[2]
    cx = x
    
    # Get font metrics for vertical alignment on the baseline
    normal_ascent, _ = normal_font.getmetrics()
    accent_ascent, _ = accent_font.getmetrics()
    baseline = y + normal_ascent

    for i, (word, is_acc) in enumerate(line_words):
        f = accent_font if is_acc else normal_font
        col = accent_color if is_acc else normal_color
        has_space = i > 0 and (word not in PUNCTUATION_ATTACH_LEFT) and (line_words[i-1][0] not in PUNCTUATION_ATTACH_RIGHT)
        if has_space:
            cx += sp_w
            
        f_ascent = accent_ascent if is_acc else normal_ascent
        draw_y = baseline - f_ascent
        
        draw.text((cx, draw_y), word, font=f, fill=col)
        cx += draw.textbbox((0, 0), word, font=f)[2]


# ── Drawing helpers ──────────────────────────────────────────────────────────

def add_grain(img, strength=7):
    """Subtle film grain overlay."""
    if not _HAS_NUMPY:
        return img
    arr = np.array(img).astype(np.int16)
    noise = np.random.randint(-strength, strength + 1, (img.height, img.width, 1), dtype=np.int16)
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), img.mode)


def new_canvas(bg_rgb):
    return Image.new("RGBA", (W, H), (*bg_rgb[:3], 255))


def make_circle_avatar(photo_path, size, ring_rgba):
    img = Image.open(photo_path).convert("RGB")
    w, h = img.size
    side = min(w, h)
    img = img.crop(((w - side) // 2, (h - side) // 2,
                    (w + side) // 2, (h + side) // 2))
    img = img.resize((size, size), Image.LANCZOS)

    ring_size = size + 6
    ring_img = Image.new("RGBA", (ring_size, ring_size), (0, 0, 0, 0))
    ImageDraw.Draw(ring_img).ellipse(
        [0, 0, ring_size - 1, ring_size - 1], outline=ring_rgba, width=3)

    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size, size], fill=255)
    circle = img.convert("RGBA")
    circle.putalpha(mask)
    return circle, ring_img


def paste_avatar(img, path, size, ring_rgba, x, y):
    circle, ring = make_circle_avatar(path, size, ring_rgba)
    img.paste(ring, (x - 3, y - 3), ring)
    img.paste(circle, (x, y), circle)


def draw_rule(draw, y, x0, x1, color_rgba):
    draw.line([(x0, y), (x1, y)], fill=color_rgba, width=1)


def draw_corner_brackets(draw, color_rgba, size=28, weight=1, inset=PAD):
    """Thin L-shaped bracket marks at top-left and bottom-right corners."""
    # Top-left
    draw.line([(inset, inset), (inset + size, inset)], fill=color_rgba, width=weight)
    draw.line([(inset, inset), (inset, inset + size)], fill=color_rgba, width=weight)
    # Bottom-right
    draw.line([(W - inset - size, H - inset), (W - inset, H - inset)],
              fill=color_rgba, width=weight)
    draw.line([(W - inset, H - inset - size), (W - inset, H - inset)],
              fill=color_rgba, width=weight)


def wrap_plain(text, font, draw, max_w):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        if draw.textbbox((0, 0), test, font=font)[2] > max_w and current:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    return lines


# ── Slide renderers ──────────────────────────────────────────────────────────

def render_cover(title, subtitle, eyebrow, name, job_title,
                 avatar_path, total_slides, theme_name, cover_image_path=None):
    c = THEMES[theme_name]
    img = new_canvas(c["bg"])
    draw = ImageDraw.Draw(img)

    bold  = find_font("bold")
    reg   = find_font("regular")
    mono  = find_font("mono")
    edit  = find_font("editorial")

    # ── Header: avatar + name + job title ────────────────────────────────────
    AVATAR = 72
    paste_avatar(img, avatar_path, AVATAR, c["ring"], PAD, PAD)
    draw = ImageDraw.Draw(img)

    f_name = ImageFont.truetype(bold, 28)
    f_jt   = ImageFont.truetype(reg,  20)
    nx = PAD + AVATAR + 20
    draw.text((nx, PAD + 8),  name,      font=f_name, fill=c["text"])
    draw.text((nx, PAD + 42), job_title, font=f_jt,   fill=c["accent"])

    # ── Rule ─────────────────────────────────────────────────────────────────
    rule_y = PAD + AVATAR + 36
    draw_rule(draw, rule_y, PAD, W - PAD, c["rule"])

    # ── Eyebrow (optional) ────────────────────────────────────────────────────
    content_top = rule_y + 64
    if eyebrow:
        f_eye = ImageFont.truetype(mono, 18)
        draw.text((PAD, content_top), eyebrow.upper(), font=f_eye, fill=c["eyebrow"])
        content_top += 44

    # ── Title block ───────────────────────────────────────────────────────────
    content_bottom = H - 110
    content_h = content_bottom - content_top
    max_w = W - PAD * 2

    segments = parse_styled(title)

    start_fs = (58, 50, 44, 38, 32) if cover_image_path else (90, 78, 68, 58, 50, 44)
    for fsize in start_fs:
        f_title_b = ImageFont.truetype(bold, fsize)
        f_title_e = ImageFont.truetype(edit, fsize)
        lines = wrap_styled(segments, f_title_b, f_title_e, draw, max_w)
        line_h = int(fsize * 1.16)
        max_pct = 0.35 if cover_image_path else 0.65
        if len(lines) * line_h < content_h * max_pct:
            break

    title_y = content_top + int(content_h * 0.08)

    y = title_y
    for line in lines:
        draw_styled_line(draw, PAD, y, line, f_title_b, f_title_e,
                         c["text"], c["accent"])
        y += line_h

    # ── Subtitle ──────────────────────────────────────────────────────────────
    if subtitle:
        f_sub = ImageFont.truetype(reg, 30)
        sub_lines = wrap_plain(subtitle, f_sub, draw, max_w)
        y += 40
        for sl in sub_lines:
            draw.text((PAD, y), sl, font=f_sub, fill=c["accent"])
            y += int(30 * 1.45)

    # ── Cover Image ───────────────────────────────────────────────────────────
    if cover_image_path and os.path.exists(cover_image_path):
        cover_img = Image.open(cover_image_path)
        if cover_img.mode != "RGBA":
            cover_img = cover_img.convert("RGBA")
        
        bot_y = H - 76
        img_y_start = y + 20
        img_y_end = bot_y - 20
        available_h = img_y_end - img_y_start
        available_w = max_w
        
        if available_h > 100:
            img_w, img_h = cover_img.size
            ratio = min(available_w / img_w, available_h / img_h)
            new_w = int(img_w * ratio)
            new_h = int(img_h * ratio)
            resized_img = cover_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            img_x = PAD + (available_w - new_w) // 2
            img_y = img_y_start + (available_h - new_h) // 2
            
            img.paste(resized_img, (img_x, img_y), resized_img)
            
            draw.rectangle([img_x - 1, img_y - 1, img_x + new_w, img_y + new_h], outline=c["rule"], width=1)

    # ── Bottom: swipe CTA + counter ───────────────────────────────────────────
    f_cta     = ImageFont.truetype(bold,  28)
    f_counter = ImageFont.truetype(mono, 22)

    bot_y = H - 76
    draw.text((PAD, bot_y), "→ Swipe", font=f_cta, fill=c["accent"])

    counter = f"1 / {total_slides}"
    cw = draw.textbbox((0, 0), counter, font=f_counter)[2]
    draw.text((W - PAD - cw, bot_y + 4), counter, font=f_counter, fill=c["cover_num"])

    return add_grain(img.convert("RGB"))


def render_content(text, slide_num, total_slides, name, theme_name):
    c = THEMES[theme_name]
    img = new_canvas(c["bg"])
    draw = ImageDraw.Draw(img)

    bold = find_font("bold")
    reg  = find_font("regular")
    mono = find_font("mono")
    edit = find_font("editorial")

    # ── Corner brackets ───────────────────────────────────────────────────────
    draw_corner_brackets(draw, c["bracket"], size=28, weight=1, inset=PAD)

    # ── Tiny header: name left, counter right ────────────────────────────────
    f_header  = ImageFont.truetype(reg,  22)
    f_counter = ImageFont.truetype(mono, 20)

    HDR_Y = PAD + 14  # gap below corner bracket
    HDR_X = PAD + 14  # same gap as top
    draw.text((HDR_X, HDR_Y), name, font=f_header, fill=c["muted"])
    counter = f"{slide_num} / {total_slides}"
    cw = draw.textbbox((0, 0), counter, font=f_counter)[2]
    draw.text((W - PAD - cw, HDR_Y + 1), counter, font=f_counter, fill=c["muted"])

    # ── Rule ─────────────────────────────────────────────────────────────────
    rule_y = HDR_Y + 38
    draw_rule(draw, rule_y, PAD, W - PAD, c["rule"])

    # ── Content block bounds ──────────────────────────────────────────────────
    content_top    = rule_y + 80
    content_bottom = H - PAD - 80
    content_h      = content_bottom - content_top
    text_x         = PAD + 32   # offset from bar
    max_w          = W - text_x - PAD

    # Parse markdown-like content
    lines = text.split("\n")
    slide_header = None
    footer_callout = None
    body_elements = []
    
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        if line_str.startswith("###") or line_str.startswith("##") or line_str.startswith("#"):
            slide_header = line_str.lstrip("#").strip()
        elif line_str.startswith(">"):
            footer_callout = line_str.lstrip(">").strip()
        elif line_str.startswith("- ") or line_str.startswith("• "):
            b_text = line_str[2:].strip()
            body_elements.append({"type": "bullet", "text": b_text})
        elif re.match(r"^\d+\.\s+", line_str):
            m = re.match(r"^(\d+)\.\s+(.*)$", line_str)
            num = int(m.group(1))
            num_text = m.group(2).strip()
            body_elements.append({"type": "number", "num": num, "text": num_text})
        else:
            body_elements.append({"type": "para", "text": line_str})

    # Layout loop over font sizes
    best_fsize = 34
    best_layout = None

    for fsize in (44, 40, 36, 32, 28):
        f_h_b = ImageFont.truetype(bold, int(fsize * 1.25))
        f_h_e = ImageFont.truetype(bold, int(fsize * 1.25))  # Use bold instead of edit for headers
        
        f_b_r = ImageFont.truetype(reg, fsize)
        f_b_e = ImageFont.truetype(bold, fsize)             # Use bold instead of edit for highlights
        
        f_f_b = ImageFont.truetype(bold, int(fsize * 0.85))
        f_f_e = ImageFont.truetype(bold, int(fsize * 0.85))  # Use bold instead of edit for footers

        layout = {
            "header": None,
            "body": [],
            "footer": None,
            "total_h": 0
        }

        current_y = 0

        # 1. Measure header
        if slide_header:
            segments = parse_styled(slide_header)
            h_lines = wrap_styled(segments, f_h_b, f_h_e, draw, max_w)
            h_line_h = int(fsize * 1.25 * 1.3)
            h_height = len(h_lines) * h_line_h
            layout["header"] = {
                "lines": h_lines,
                "line_h": h_line_h,
                "height": h_height,
                "font_b": f_h_b,
                "font_e": f_h_e
            }
            current_y += h_height + 40 # gap below header

        # 2. Measure body elements
        for elem in body_elements:
            elem_type = elem["type"]
            elem_text = elem["text"]
            
            segments = parse_styled(elem_text)
            el_max_w = max_w - 40 if elem_type in ("bullet", "number") else max_w
            
            el_lines = wrap_styled(segments, f_b_r, f_b_e, draw, el_max_w)
            el_line_h = int(fsize * 1.45)
            el_height = len(el_lines) * el_line_h
            
            layout["body"].append({
                "type": elem_type,
                "num": elem.get("num"),
                "lines": el_lines,
                "line_h": el_line_h,
                "height": el_height,
                "font_r": f_b_r,
                "font_e": f_b_e
            })
            current_y += el_height + 24 # gap below elements
        
        if layout["body"]:
            current_y -= 24 # remove last element's gap

        layout["total_h"] = current_y

        # 3. Measure footer callout
        footer_h = 0
        if footer_callout:
            segments = parse_styled(footer_callout)
            # Indented box max width: W - (PAD + 24) * 2 - 48
            box_max_w = W - (PAD + 24) * 2 - 48
            f_lines = wrap_styled(segments, f_f_b, f_f_e, draw, box_max_w)
            f_line_h = int(fsize * 0.85 * 1.4)
            text_h = len(f_lines) * f_line_h
            box_h = text_h + 36
            
            layout["footer"] = {
                "lines": f_lines,
                "line_h": f_line_h,
                "height": box_h,
                "font_b": f_f_b,
                "font_e": f_f_e
            }
            footer_h = box_h + 40
            
        if current_y + footer_h <= content_h:
            best_fsize = fsize
            best_layout = layout
            break
            
    if not best_layout:
        best_layout = layout
        best_fsize = fsize

    # Calculate actual left vertical accent bar bottom
    box_h = best_layout["footer"]["height"] if best_layout["footer"] else 0
    box_y = H - PAD - 20 - box_h
    bar_bottom = box_y - 20 if best_layout["footer"] else (H - PAD - 80)

    # Draw left vertical accent bar
    bar_top = rule_y + 80
    bar_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bar_draw  = ImageDraw.Draw(bar_layer)
    bar_col   = (*c["accent"][:3], 60)
    bar_draw.rectangle([PAD, bar_top, PAD + 2, bar_bottom], fill=bar_col)
    img = Image.alpha_composite(img, bar_layer)
    draw = ImageDraw.Draw(img)

    # Calculate starting y for content to center it vertically
    remaining_h = content_h - (box_h + 40 if best_layout["footer"] else 0)
    content_y_start = content_top + max(0, (remaining_h - best_layout["total_h"]) // 2)
    
    y = content_y_start

    # Draw header
    if best_layout["header"]:
        l_info = best_layout["header"]
        for line in l_info["lines"]:
            draw_styled_line(draw, text_x, y, line, l_info["font_b"], l_info["font_e"],
                             c["text"], c["accent"])
            y += l_info["line_h"]
        y += 40

    # Draw body elements
    for el in best_layout["body"]:
        el_type = el["type"]
        draw_x = text_x
        if el_type in ("bullet", "number"):
            draw_x = text_x + 40
            marker_y = y + int(best_fsize * 0.15)
            if el_type == "bullet":
                draw.ellipse([text_x + 10, marker_y + 10, text_x + 20, marker_y + 20], fill=c["accent"])
            else:
                f_num = el["font_r"]
                draw.text((text_x + 6, y), f"{el['num']}.", font=f_num, fill=c["accent"])
                
        for line in el["lines"]:
            draw_styled_line(draw, draw_x, y, line, el["font_r"], el["font_e"],
                             c["text"], c["accent"])
            y += el["line_h"]
        y += 24

    # Draw footer callout box
    if best_layout["footer"]:
        f_info = best_layout["footer"]
        
        # Coordinates for floating rounded box
        box_x0 = PAD + 24
        box_x1 = W - PAD - 24
        
        # Draw background rounded rectangle
        box_bg = (*c["accent"][:3], 240) if theme_name == "dark" else (*c["accent"][:3], 255)
        draw.rounded_rectangle([box_x0, box_y, box_x1, box_y + box_h], radius=16, fill=box_bg)
        
        # Text color inside the box
        text_color_in_box = c["bg"]
        accent_color_in_box = (255, 255, 255, 255) if theme_name == "dark" else (245, 241, 234, 255)
        
        # Draw lines centered
        fy = box_y + 18
        for line in f_info["lines"]:
            lw = measure_line(line, f_info["font_b"], f_info["font_e"], draw)
            lx = box_x0 + (box_x1 - box_x0 - lw) // 2
            draw_styled_line(draw, lx, fy, line, f_info["font_b"], f_info["font_e"],
                             text_color_in_box, accent_color_in_box)
            fy += f_info["line_h"]

    return add_grain(img.convert("RGB"))


def render_cta(cta_text, name, job_title, avatar_path, theme_name, website=None):
    c = THEMES[theme_name]
    img = new_canvas(c["bg"])
    draw = ImageDraw.Draw(img)

    bold = find_font("bold")
    reg  = find_font("regular")
    mono = find_font("mono")

    # ── Corner brackets ───────────────────────────────────────────────────────
    draw_corner_brackets(draw, c["bracket"], size=28, weight=1, inset=PAD)
    draw = ImageDraw.Draw(img)

    # ── Large avatar centered ─────────────────────────────────────────────────
    AVATAR = 160
    ax = (W - AVATAR) // 2
    ay = int(H * 0.20)
    paste_avatar(img, avatar_path, AVATAR, c["ring"], ax, ay)
    draw = ImageDraw.Draw(img)

    # ── Name + job title ──────────────────────────────────────────────────────
    f_name = ImageFont.truetype(bold, 48)
    f_jt   = ImageFont.truetype(reg,  30)

    name_y = ay + AVATAR + 36
    nw = draw.textbbox((0, 0), name, font=f_name)[2]
    draw.text(((W - nw) // 2, name_y), name, font=f_name, fill=c["text"])

    jw = draw.textbbox((0, 0), job_title, font=f_jt)[2]
    draw.text(((W - jw) // 2, name_y + 62), job_title, font=f_jt, fill=c["accent"])

    # ── Rule ─────────────────────────────────────────────────────────────────
    rule_y = name_y + 62 + 44 + 32
    draw_rule(draw, rule_y, PAD * 2, W - PAD * 2, c["rule"])

    # ── CTA text ─────────────────────────────────────────────────────────────
    f_cta  = ImageFont.truetype(bold, 44)
    max_w  = W - PAD * 3
    cta_lines = wrap_plain(cta_text, f_cta, draw, max_w)
    line_h = int(44 * 1.26)

    cta_y = rule_y + 56
    for line in cta_lines:
        lw = draw.textbbox((0, 0), line, font=f_cta)[2]
        draw.text(((W - lw) // 2, cta_y), line, font=f_cta, fill=c["text"])
        cta_y += line_h

    # ── Website ───────────────────────────────────────────────────────────────
    if website:
        f_web = ImageFont.truetype(mono, 26)
        ww = draw.textbbox((0, 0), website, font=f_web)[2]
        draw.text(((W - ww) // 2, cta_y + 32), website, font=f_web, fill=c["muted"])

    return add_grain(img.convert("RGB"))


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--title",      required=True,
                   help="Cover headline. Use **phrase** to accent a phrase.")
    p.add_argument("--subtitle",   default=None)
    p.add_argument("--eyebrow",    default=None,
                   help="Mono eyebrow text above title, e.g. 'AI SECURITY · LESSON LEARNED'")
    p.add_argument("--slides",     required=True,
                   help='JSON array of content slide texts')
    default_avatar = str(Path(__file__).resolve().parent.parent / "assets" / "default_avatar.png")
    p.add_argument("--cta",        default="Follow for more technical insights")
    p.add_argument("--slug",       required=True)
    p.add_argument("--output-dir", default="./carousels",
                   help="Parent dir for carousels. Output goes to {dir}/{slug}_{date}/")
    p.add_argument("--avatar",     default=default_avatar,
                   help="Path to avatar image file")
    p.add_argument("--name",       default="Alex Rivers")
    p.add_argument("--job-title",  default="AI Engineer & Systems Architect")
    p.add_argument("--theme",      default="dark",
                   choices=["dark", "paper", "cream"])
    p.add_argument("--website",    default="example.com")
    p.add_argument("--no-cta",      action="store_true")
    p.add_argument("--both-themes", action="store_true",
                   help="Generate two PDFs: dark and paper (light) themes")
    p.add_argument("--cover-image", default=None,
                   help="Path to screenshot or image to display on the cover slide")
    args = p.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    themes = ["dark", "paper"] if args.both_themes else [args.theme]

    title = clean_text_str(args.title)
    subtitle = clean_text_str(args.subtitle) if args.subtitle else None
    eyebrow = clean_text_str(args.eyebrow) if args.eyebrow else None
    cta = clean_text_str(args.cta)

    for theme in themes:
        raw_slides = json.loads(args.slides)
        content_slides = [clean_text_str(s) for s in raw_slides]
        has_cta = not args.no_cta
        total = 1 + len(content_slides) + (1 if has_cta else 0)

        slides = []

        cover = render_cover(
            title=title,
            subtitle=subtitle,
            eyebrow=eyebrow,
            name=args.name,
            job_title=args.job_title,
            avatar_path=args.avatar,
            total_slides=total,
            theme_name=theme,
            cover_image_path=args.cover_image,
        )
        slides.append(cover)

        for i, text in enumerate(content_slides, 2):
            slide = render_content(
                text=text,
                slide_num=i,
                total_slides=total,
                name=args.name,
                theme_name=theme,
            )
            slides.append(slide)

        if has_cta:
            cta_slide = render_cta(
                cta_text=cta,
                name=args.name,
                job_title=args.job_title,
                avatar_path=args.avatar,
                theme_name=theme,
                website=args.website,
            )
            slides.append(cta_slide)

        suffix = f"_{theme}" if args.both_themes else ""
        out_pdf = os.path.join(args.output_dir, f"carousel_{args.slug}{suffix}.pdf")
        slides[0].save(out_pdf, save_all=True, append_images=slides[1:])
        try:
            clean_file_path(out_pdf, in_place=True)
        except Exception:
            pass
        print(f"Saved: {out_pdf}")

    print(f"\nDone: {len(slides)} slides per theme")


if __name__ == "__main__":
    main()
