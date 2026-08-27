from pathlib import Path
from html import escape

INPUT = "portrait.txt"
OUTPUT = "portrait_tspan.txt"

# Card geometry in SVG:
# Left Card: x=14, y=26, width=488, height=468
# Center X = 14 + 488/2 = 258
# Top Y = 26, Bottom Y = 494, Center Y = 260
START_X = 258
LINE_HEIGHT = 7.7

# Optional trimming
TRIM_LEFT = 0
TRIM_RIGHT = 0
REMOVE_EMPTY = False

lines = Path(INPUT).read_text(
    encoding="utf-8",
    errors="ignore"
).splitlines()

lines = [l.rstrip() for l in lines]

if REMOVE_EMPTY:
    lines = [l for l in lines if l.strip()]

processed = []
for line in lines:
    if TRIM_RIGHT > 0:
        line = line[:-TRIM_RIGHT]
    if TRIM_LEFT > 0:
        line = line[TRIM_LEFT:]
    processed.append(line)

num_lines = len(processed)
# Calculate start_y so the entire ASCII block is centered vertically in the card (y: 26 to 494)
total_text_height = (num_lines - 1) * LINE_HEIGHT
card_top = 26
card_height = 468
top_padding = (card_height - total_text_height) / 2
START_Y = round(card_top + top_padding + 5.5, 2)

svg = []
for i, line in enumerate(processed):
    y = round(START_Y + i * LINE_HEIGHT, 2)
    svg.append(
        f'<tspan x="{START_X}" y="{y}">{escape(line)}</tspan>'
    )

Path(OUTPUT).write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print(f"Generated {len(svg)} tspans with START_X={START_X}, START_Y={START_Y}, LINE_HEIGHT={LINE_HEIGHT}")