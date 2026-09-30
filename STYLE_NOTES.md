# Carousel Style Notes

Style preferences and overrides recorded during use.
Format: [YYYY-MM-DD] Rule or preference.

[2026-06-07] NEVER rewrite or improve slide text. Take the user's text exactly as-is and only split it into slides. No rewording, no polish, no paraphrasing.
[2026-06-07] CTA slide: keep it minimal — just avatar, name, and "Follow" (or "Подписывайся"). No custom CTA text unless explicitly asked.
[2026-06-07] ALWAYS run linkedin_post_creator skill first before making the carousel (grammar fix + EN translation). Carousel uses the approved EN text.
[2026-06-30] Highlighted text inside content slides must be Geist-Bold (bold weight, accent color), not FrauncesItalic. Cover titles still use FrauncesItalic.
[2026-06-30] Bottom callout boxes must be floating cards (24px horizontal margins) with 16px rounded corners, and left vertical bar must terminate above them.
[2026-06-30] Use high-contrast logo silhouettes (like white-on-dark logos) to prevent them blending into backgrounds.
[2026-09-24] Visual hero images: section height is 600px (matching 3:2 and 16:9 landscape aspect ratios). Default is borderless & seamless (no outer bounding box or frame border around illustrations), allowing artwork to blend naturally into the slide canvas without awkward side bars. If a framed card is explicitly requested (framed: true), use object-fit: cover so the image fills the frame completely edge-to-edge.
