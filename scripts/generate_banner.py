"""One-time generator for assets/hero-banner.svg.

Not run in CI — committed for reproducibility. The banner is a field of
binary digits drifting upward; inside the letterforms of the name the same
digits run brighter and denser, so the text literally emerges from the
primitives. SMIL only (renders on GitHub via <img>).
"""
import random

random.seed(20260717)

W, H = 1200, 300
INDIGO, TEAL, GOLD = "#4f46e5", "#0ea5a4", "#eab308"
DIM = ["#293049", "#2f3a5c", "#26314e", "#334066"]

parts = []
parts.append(
    f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    'xmlns="http://www.w3.org/2000/svg" role="img" '
    'aria-label="Sai Teja Meka — AI/ML Engineer — verified systems from minimal primitives">'
)
parts.append(
    '<defs>'
    '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0%" stop-color="#0b0e1a"/><stop offset="100%" stop-color="#101528"/>'
    '</linearGradient>'
    '<linearGradient id="name" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0%" stop-color="{INDIGO}"/>'
    f'<stop offset="55%" stop-color="{TEAL}"/>'
    f'<stop offset="100%" stop-color="{GOLD}"/>'
    '</linearGradient>'
    '<clipPath id="letters">'
    '<text x="600" y="172" text-anchor="middle" '
    'font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="86" '
    'font-weight="800" letter-spacing="10">SAI TEJA MEKA</text>'
    '</clipPath>'
    '</defs>'
)
parts.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

# --- background field: dim digits drifting upward ---
parts.append('<g font-family="Consolas, Menlo, monospace" font-size="13">')
for i in range(150):
    x = round(random.uniform(8, W - 8), 1)
    y = round(random.uniform(-20, H + 20), 1)
    d = random.choice("01")
    c = random.choice(DIM)
    dur = round(random.uniform(14, 30), 1)
    delay = round(random.uniform(-30, 0), 1)
    op = round(random.uniform(0.25, 0.7), 2)
    parts.append(
        f'<text x="{x}" y="{y}" fill="{c}" opacity="{op}">{d}'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 40" to="0 -{H + 60}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
        '</text>'
    )
parts.append('</g>')

# --- the name: dark base plate + bright digits rising inside the letterforms ---
parts.append('<g clip-path="url(#letters)">')
parts.append('<rect x="140" y="90" width="920" height="100" fill="#151b33"/>')
parts.append('<g font-family="Consolas, Menlo, monospace" font-size="12" font-weight="700">')
for i in range(360):
    x = round(random.uniform(150, 1050), 1)
    y = round(random.uniform(80, 200), 1)
    d = random.choice("01")
    c = random.choices([INDIGO, TEAL, GOLD, "#8f95f8"], weights=[4, 4, 2, 3])[0]
    dur = round(random.uniform(5, 12), 1)
    delay = round(random.uniform(-12, 0), 1)
    parts.append(
        f'<text x="{x}" y="{y}" fill="{c}">{d}'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 30" to="0 -130" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.7;1" '
        f'dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
        '</text>'
    )
parts.append('</g></g>')

# --- legibility pass: translucent gradient fill + hairline stroke over the digits ---
parts.append(
    '<text x="600" y="172" text-anchor="middle" '
    'font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="86" '
    'font-weight="800" letter-spacing="10" fill="url(#name)" opacity="0.28">SAI TEJA MEKA</text>'
)
parts.append(
    '<text x="600" y="172" text-anchor="middle" '
    'font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="86" '
    'font-weight="800" letter-spacing="10" fill="none" stroke="url(#name)" '
    'stroke-width="1.2" opacity="0.85">SAI TEJA MEKA</text>'
)

# --- subtitle ---
parts.append(
    '<text x="600" y="224" text-anchor="middle" '
    'font-family="Consolas, Menlo, monospace" font-size="17" fill="#7c8db5" '
    'letter-spacing="2">AI/ML Engineer — verified systems from minimal primitives'
    '<animate attributeName="opacity" values="0;1" dur="2.5s" fill="freeze"/></text>'
)
parts.append('</svg>')

svg = "".join(parts)
with open("assets/hero-banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"hero-banner.svg: {len(svg) / 1024:.1f} KB")
