#!/usr/bin/env python3
"""Draw the front page for 20 November 2026 and write entry.png.

A newspaper front page, drawn from scratch with Pillow: one masthead,
one lead story, two picture stories and three short columns, plus a
footer strip of briefs. All text and art is generated here; no photo or
clip art is used. Run:  python3 draw_frontpage.py  (writes entry.png
next to this file, 1024x1024, under 1 MiB).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 230)
INK = (24, 24, 22)
RED = (139, 26, 26)
NAVY = (18, 38, 66)
TEAL = (14, 90, 86)
GREY = (92, 88, 80)
LIGHT = (255, 252, 244)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, max_w, text, fnt, fill=INK, leading=None):
    """Draw a wrapped paragraph; return the y just below the last line."""
    leading = leading or int(fnt.size * 1.32)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, max_w, text, fnt, leading=None):
    """Draw a wrapped headline; return the y just below the last line."""
    leading = leading or int(fnt.size * 1.12)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=INK)
        y += leading
    return y


def kicker(draw, x, y, text, size=17, fill=RED):
    draw.text((x, y), text, font=font(SANS_B, size), fill=fill)
    return y + size + 8


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_calendar(d, x, y, w, h):
    """A wall calendar turned to January 2027, the 1st circled in red."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=LIGHT,
                        outline=INK, width=3)
    d.rounded_rectangle([x, y, x + w, y + 52], radius=14, fill=RED)
    d.rectangle([x, y + 40, x + w, y + 52], fill=RED)
    d.text((x + w // 2, y + 8), "2027", font=font(SERIF_B, 34),
           fill=(255, 255, 255), anchor="ma")
    d.text((x + w // 2, y + 66), "JANUARY", font=font(SANS_B, 20),
           fill=INK, anchor="ma")
    cell = 27
    gx, gy = x + 22, y + 96
    for r in range(5):
        for c in range(7):
            cx, cy = gx + c * cell, gy + r * cell
            day = r * 7 + c + 1
            if day > 31:
                continue
            if day == 1:
                d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13],
                          outline=RED, width=4)
                d.text((cx, cy), "1", font=font(SANS_B, 18), fill=RED,
                       anchor="mm")
            else:
                d.text((cx, cy), str(day), font=font(SANS, 15), fill=GREY,
                       anchor="mm")
    d.text((x + w // 2, y + h - 26), "Decision waits until next year",
           font=font(SANS, 16), fill=GREY, anchor="ma")


def draw_cyclone(d, x, y, w, h):
    """A storm spiral over a coastline: concentric arcs and rain."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=(214, 228, 238),
                        outline=INK, width=2)
    cx, cy = x + w // 2, y + h // 2 - 4
    for i, r in enumerate(range(44, 8, -12)):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200 + i * 38,
              end=200 + i * 38 + 250, fill=NAVY, width=5)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)
    for i in range(12):
        rx = x + 14 + i * 38
        d.line([(rx, y + h - 46), (rx - 8, y + h - 32)], fill=NAVY, width=3)
    d.rectangle([x, y + h - 28, x + w, y + h], fill=(120, 150, 120))
    d.text((x + 10, y + h - 24), "ODISHA COAST",
           font=font(SANS_B, 14), fill=(255, 255, 255))


def draw_voyager(d, x, y, w, h):
    """Voyager 1 against the stars, a day of light from home."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=(10, 16, 34),
                        outline=INK, width=2)
    import random
    rnd = random.Random(20261120)
    for _ in range(70):
        sx, sy = x + rnd.randint(6, w - 6), y + rnd.randint(6, h - 6)
        r = rnd.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r],
                  fill=(255, 255, 255) if rnd.random() > 0.2 else (180, 200, 255))
    bx, by = x + w - 118, y + 34
    d.line([(bx, by + 16), (bx - 34, by - 6)], fill=(200, 170, 80), width=3)
    d.line([(bx, by + 16), (bx - 30, by + 40)], fill=(200, 170, 80), width=3)
    d.rectangle([bx, by, bx + 46, by + 34], fill=(212, 175, 55),
                outline=(120, 95, 20), width=2)
    d.ellipse([bx - 12, by - 26, bx + 26, by + 8], fill=(230, 230, 230),
              outline=(150, 150, 150), width=2)
    d.line([(bx + 8, by + 34), (bx + 8, by + 56)], fill=(200, 170, 80), width=3)
    d.ellipse([bx - 2, by + 52, bx + 18, by + 72], fill=(200, 170, 80))
    for i in range(5):
        ex = x + w - 260 + i * 24
        ey = y + h - 46
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(120, 200, 120))
    d.text((x + 12, y + h - 26), "ONE LIGHT-DAY FROM EARTH",
           font=font(SANS_B, 14), fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 10, H - 10], outline=INK, width=3)
    d.rectangle([18, 18, W - 18, H - 18], outline=INK, width=1)

    # ---- Masthead ----
    d.text((W // 2, 44), "THE WORLD IN ONE DAY", font=font(SERIF_B, 62),
           fill=INK, anchor="ma")
    rule(d, 34, 122, W - 34, 2)
    d.text((34, 132), "FRIDAY, 20 NOVEMBER 2026",
           font=font(SANS_B, 21), fill=INK)
    d.text((W - 34, 132), "ONE DAY  •  ONE PAGE  •  THE WHOLE WORLD",
           font=font(SANS, 17), fill=GREY, anchor="ra")
    rule(d, 34, 166, W - 34, 4)

    # ---- Lead story: Trump / Iran ----
    y = 186
    y = kicker(d, 34, y, "WASHINGTON  —  THE IRAN DECISION", 18)
    y = headline(d, 34, y, 600, "Trump puts Iran decision off until 2027",
                 font(SERIF_B, 48), leading=54)
    y += 8
    para(d, 34, y, 600,
         "The president says there is \u201cno rush\u201d on war with Iran "
         "and he will \u201csee what happens\u201d after 1 January.",
         font(SERIF, 22), leading=30)
    draw_calendar(d, 668, 186, 322, 254)
    rule(d, 34, 452, W - 34, 2)

    # ---- Row two: cyclone and Voyager ----
    y = 470
    kicker(d, 34, y, "INDIA  —  CYCLONE AKVAN", 17)
    draw_cyclone(d, 34, 500, 462, 112)
    headline(d, 34, 624, 462, "Cyclone Akvan bears down on Odisha",
             font(SERIF_B, 30), leading=33)
    para(d, 34, 694, 462,
         "300,000 evacuated and 423 rescue teams on standby as the "
         "storm nears India\u2019s east coast.",
         font(SERIF, 19), leading=25)

    d.line([(512, 470), (512, 756)], fill=INK, width=1)
    kicker(d, 536, y, "SPACE  —  VOYAGER 1", 17)
    draw_voyager(d, 536, 500, 454, 112)
    headline(d, 536, 624, 454, "Voyager 1 crosses one light-day from Earth",
             font(SERIF_B, 30), leading=33)
    para(d, 536, 694, 454,
         "NASA confirms the 1977 probe is a full light-day away \u2014 "
         "a signal now takes 24 hours.",
         font(SERIF, 19), leading=25)
    rule(d, 34, 762, W - 34, 2)

    # ---- Row three: three short columns ----
    y = 778
    cols = [
        (34, 300, "EUROPE", "Europe open to Ukraine talks with Russia",
         "European leaders are open to talks with Moscow to end the war."),
        (362, 300, "THE HAGUE", "Myanmar guilty of genocide, UN court rules",
         "UN court: Myanmar committed genocide against the Rohingya."),
        (690, 300, "JAPAN  —  SPACE", "Engine trouble ends Hayabusa2 landing plan",
         "Japan\u2019s probe must change course after a fault rules out its landing."),
    ]
    for cx, cw, kick, head, body in cols:
        kicker(d, cx, y, kick, 15)
        yy = headline(d, cx, 804, cw, head, font(SERIF_B, 23), leading=26)
        para(d, cx, yy + 4, cw, body, font(SERIF, 16), leading=21)
    d.line([(346, 778), (346, 930)], fill=INK, width=1)
    d.line([(674, 778), (674, 930)], fill=INK, width=1)
    rule(d, 34, 936, W - 34, 2)

    # ---- Footer: briefs ----
    d.text((34, 948), "ALSO TODAY", font=font(SANS_B, 16), fill=RED)
    para(d, 34, 972, 956,
         "GTA 6 sales pass $1.8bn  •  Phillips century lifts New Zealand to "
         "317\u20136  •  Migrant boat sinks off Senegal; dozens missing",
         font(SANS, 16), leading=20)
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
