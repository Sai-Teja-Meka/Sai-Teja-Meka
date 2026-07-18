"""Daily generative art — deterministic from today's date, stdlib only.

One rule, new seed each day: a damped Lissajous curve whose frequency pair,
phase, and damping come from sha256(YYYY-MM-DD). 200-400 elements (dots,
short strokes tangent to the curve, and binary digits) are sampled along the
trajectory onto a sparse dark field. A handful of elements get a slow SMIL
opacity drift. Palette: indigo #4f46e5 / teal #0ea5a4 / gold #eab308.
"""
import datetime
import hashlib
import math
import random

W, H = 1200, 480
INDIGO, TEAL, GOLD = "#4f46e5", "#0ea5a4", "#eab308"
SLATE = ["#2b3352", "#333d63", "#3a466f"]

today = datetime.date.today().isoformat()
seed = int.from_bytes(hashlib.sha256(today.encode()).digest()[:8], "big")
rng = random.Random(seed)

# --- the rule's parameters, varied by seed ---
a = rng.choice([2, 3, 4, 5, 7])            # x frequency
b = rng.choice([3, 4, 5, 6, 8])            # y frequency
phase = rng.uniform(0, math.pi)            # phase offset
damp = rng.uniform(0.015, 0.09)            # radial damping (kept low so the curve fills the frame)
n = rng.randint(240, 380)                  # element count
rot = rng.uniform(0, math.pi)              # frame rotation

cx, cy, rx, ry = W / 2, H / 2, W * 0.38, H * 0.36
cos_r, sin_r = math.cos(rot), math.sin(rot)


def point(t):
    decay = math.exp(-damp * t)
    x = math.sin(a * t + phase) * decay
    y = math.sin(b * t) * decay
    xr = x * cos_r - y * sin_r
    yr = x * sin_r + y * cos_r
    return cx + xr * rx, cy + yr * ry


parts = [
    f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    'xmlns="http://www.w3.org/2000/svg" role="img" '
    f'aria-label="Generative art for {today}">',
    f'<rect width="{W}" height="{H}" fill="#0b0e1a"/>',
    '<g font-family="Consolas, Menlo, monospace">',
]

t_max = 14 * math.pi
animated_budget = 12
for i in range(n):
    t = (i / n) * t_max
    x, y = point(t)
    x += rng.uniform(-6, 6)
    y += rng.uniform(-6, 6)
    if not (0 < x < W and 0 < y < H):
        continue
    roll = rng.random()
    # mostly quiet slate, sparse accents
    color = (
        rng.choice(SLATE) if roll < 0.62
        else INDIGO if roll < 0.78
        else TEAL if roll < 0.92
        else GOLD
    )
    anim = ""
    if animated_budget > 0 and roll > 0.9:
        animated_budget -= 1
        dur = round(rng.uniform(6, 14), 1)
        anim = (
            f'<animate attributeName="opacity" values="0.25;0.9;0.25" '
            f'dur="{dur}s" repeatCount="indefinite"/>'
        )
    kind = rng.random()
    if kind < 0.45:  # dot
        r = round(rng.uniform(1.0, 2.4), 1)
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" '
            f'opacity="{rng.uniform(0.4, 0.9):.2f}">{anim}</circle>'
        )
    elif kind < 0.8:  # short stroke tangent to the curve
        x2, y2 = point(t + 0.035)
        dx, dy = x2 - x, y2 - y
        norm = math.hypot(dx, dy) or 1
        ln = rng.uniform(5, 14)
        parts.append(
            f'<line x1="{x:.1f}" y1="{y:.1f}" '
            f'x2="{x + dx / norm * ln:.1f}" y2="{y + dy / norm * ln:.1f}" '
            f'stroke="{color}" stroke-width="1.1" '
            f'opacity="{rng.uniform(0.35, 0.8):.2f}">{anim}</line>'
        )
    else:  # binary digit
        parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{rng.choice([10, 11, 12])}" '
            f'fill="{color}" opacity="{rng.uniform(0.4, 0.85):.2f}">'
            f'{rng.choice("01")}{anim}</text>'
        )

parts.append('</g>')
parts.append(
    f'<text x="24" y="{H - 20}" font-family="Consolas, Menlo, monospace" '
    f'font-size="13" fill="#4a5578">{today} · sin({a}t+φ)·e^(−λt), sin({b}t) · '
    f'seed {seed & 0xFFFFFF:06x}</text>'
)
parts.append('</svg>')

svg = "".join(parts)
with open("assets/daily.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"daily.svg for {today}: {len(svg) / 1024:.1f} KB, rule=({a},{b}), damp={damp:.3f}")
