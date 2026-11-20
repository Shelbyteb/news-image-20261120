#!/usr/bin/env python3
"""Draw the front page for 'The World in One Day - 20 November 2026'.

A newspaper front page drawn from scratch with Pillow: masthead, one lead
story with a drawn illustration, five more stories with small drawn icons,
and a bottom ticker. All stories are the news of Friday 20 November 2026
as reported that day: Cyclone Akvan's landfall in India, the COP31 final
plenary in Antalya, strikes on embassies in Kyiv, the first Trump-Xi-Putin
three-way talks at APEC in Shenzhen, Fiji's drought disaster, and the
South Korean court clearing former PM Han Duck-soo.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (20, 33, 61)
TEAL = (23, 94, 110)
GOLD = (201, 162, 39)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
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


def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=1.28):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def rule(draw, y, weight=2, x0=36, x1=988):
    draw.line([(x0, y), (x1, y)], fill=INK, width=weight)


def kicker_head_body(draw, x, y, w, kick, head, body, head_size=26,
                     body_size=18, kick_color=RED):
    f_kick = font(SANS_B, 16)
    f_head = font(SERIF_B, head_size)
    f_body = font(SANS, body_size)
    draw.text((x, y), kick, font=f_kick, fill=kick_color)
    y += 24
    y = draw_lines(draw, x, y, wrap(draw, head, f_head, w), f_head,
                   leading=1.12)
    y += 4
    y = draw_lines(draw, x, y, wrap(draw, body, f_body, w), f_body,
                   leading=1.3)
    return y


# ---------- illustration helpers ----------

def cyclone_panel(draw, box):
    """Spiral storm over a coastline, drawn with arcs and rain streaks."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=(215, 232, 239),
                           outline=TEAL, width=2)
    cx, cy = (x0 + x1) // 2 - 10, (y0 + y1) // 2 - 20
    for r, start, end in [(120, 20, 300), (95, 140, 420), (70, 260, 540),
                          (45, 20, 300), (22, 140, 420)]:
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, end,
                 fill=TEAL, width=7)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(245, 248, 250),
                 outline=TEAL, width=3)
    # coastline and sea at the bottom
    draw.polygon([(x0, y1), (x0, y1 - 46), (x0 + 130, y1 - 78),
                  (x0 + 260, y1 - 52), (x1, y1 - 66), (x1, y1)],
                 fill=(196, 164, 120))
    draw.line([(x0, y1 - 46), (x0 + 130, y1 - 78), (x0 + 260, y1 - 52),
               (x1, y1 - 66)], fill=(120, 90, 60), width=3)
    for rx in range(x0 + 20, x1 - 10, 34):
        draw.line([(rx, y0 + 14), (rx - 8, y0 + 34)], fill=(90, 140, 160),
                  width=3)


def sun_icon(draw, box, colour=(232, 164, 32)):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        draw.line([(cx + 26 * math.cos(a), cy + 26 * math.sin(a)),
                   (cx + 40 * math.cos(a), cy + 40 * math.sin(a))],
                  fill=colour, width=5)
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=colour)


def building_icon(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle([x0 + 14, y0 + 22, x1 - 14, y1 - 8], fill=(120, 128, 140),
                   outline=INK, width=2)
    for wy in range(y0 + 32, y1 - 14, 18):
        for wx in range(x0 + 22, x1 - 22, 18):
            draw.rectangle([wx, wy, wx + 9, wy + 10], fill=(240, 236, 220))
    draw.rectangle([x0 + 30, y1 - 26, x0 + 44, y1 - 8], fill=INK)
    # small two-tone flag on the roof
    draw.line([(x0 + 52, y0 + 22), (x0 + 52, y0 + 2)], fill=INK, width=3)
    draw.rectangle([x0 + 52, y0 + 2, x0 + 76, y0 + 10], fill=(38, 90, 180))
    draw.rectangle([x0 + 52, y0 + 10, x0 + 76, y0 + 18], fill=(240, 200, 40))


def flags_icon(draw, box):
    x0, y0, x1, y1 = box
    fw, fh = 26, 18
    gap = 8
    # US flag, simplified
    ux = x0 + 6
    uy = y0 + 26
    for i in range(7):
        draw.rectangle([ux, uy + i * 3, ux + fw, uy + i * 3 + 3],
                       fill=RED if i % 2 == 0 else (245, 245, 245))
    draw.rectangle([ux, uy, ux + 11, uy + 9], fill=(30, 60, 140))
    # China flag
    cx = ux + fw + gap
    draw.rectangle([cx, uy, cx + fw, uy + fh], fill=(222, 41, 16))
    draw.ellipse([cx + 4, uy + 4, cx + 9, uy + 9], fill=(255, 222, 0))
    # Russia flag
    rx = cx + fw + gap
    for i, col in enumerate([(245, 245, 245), (30, 90, 200), (200, 30, 30)]):
        draw.rectangle([rx, uy + i * 6, rx + fw, uy + i * 6 + 6], fill=col)
    draw.rectangle([x0, y0 + 52, x1, y0 + 54], fill=INK)


def drought_icon(draw, box):
    x0, y0, x1, y1 = box
    draw.ellipse([x0 + 30, y0 + 6, x0 + 62, y0 + 38], fill=(232, 164, 32))
    draw.polygon([(x0, y1), (x0, y1 - 26), (x0 + 40, y1 - 14),
                  (x0 + 70, y1 - 30), (x1, y1 - 18), (x1, y1)],
                 fill=(198, 158, 104))
    draw.line([(x0 + 12, y1 - 22), (x0 + 34, y1 - 10), (x0 + 52, y1 - 24),
               (x0 + 78, y1 - 12)], fill=(120, 84, 48), width=3)


def court_icon(draw, box):
    x0, y0, x1, y1 = box
    draw.polygon([(x0 + 8, y0 + 26), (x0 + 48, y0 + 6), (x0 + 88, y0 + 26)],
                 fill=(150, 140, 120), outline=INK)
    for cx in (x0 + 20, x0 + 44, x0 + 68):
        draw.rectangle([cx, y0 + 28, cx + 8, y1 - 10], fill=(120, 110, 96))
    draw.rectangle([x0 + 8, y1 - 10, x0 + 88, y1 - 4], fill=(120, 110, 96))


# ---------- page ----------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    f_mast = font(SERIF_B, 56)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 24), title, font=f_mast, fill=INK)
    rule(d, 96)
    f_date = font(SANS_B, 21)
    date_line = "FRIDAY, 20 NOVEMBER 2026  •  WORLD CHILDREN'S DAY"
    dw = d.textlength(date_line, font=f_date)
    d.text(((W - dw) / 2, 108), date_line, font=f_date, fill=INK)
    rule(d, 140)

    # lead story: Cyclone Akvan
    lead_y = 156
    cyclone_panel(d, (616, lead_y, 988, lead_y + 264))
    kicker_head_body(
        d, 36, lead_y, 556,
        "INDIA  •  CYCLONE AKVAN",
        "Akvan slams into India's east coast",
        "Severe Cyclonic Storm Akvan made landfall at midday "
        "across Andhra Pradesh and Odisha, with gusts of "
        "110 km/h. More than 300,000 people were moved to "
        "shelters as schools shut and the coasts braced.",
        head_size=40, body_size=20)
    rule(d, 440)

    # row 2: COP31 and Ukraine
    row2_y = 458
    sun_icon(d, (36, row2_y, 132, row2_y + 96))
    kicker_head_body(
        d, 148, row2_y, 352,
        "CLIMATE  •  COP31, ANTALYA",
        "Climate talks end without a fossil-fuel pledge",
        "The final plenary closed on a draft that drops the "
        "phase-out promise, drawing a backlash from delegates.",
        head_size=25, body_size=18)
    d.line([(512, row2_y), (512, row2_y + 190)], fill=INK, width=2)
    building_icon(d, (536, row2_y, 632, row2_y + 96))
    kicker_head_body(
        d, 648, row2_y, 340,
        "UKRAINE  •  KYIV",
        "Strikes damage embassies in Kyiv",
        "Russian strikes hit the Austrian and Dutch embassies. "
        "Ukraine says it struck the Crimean Bridge rail link.",
        head_size=25, body_size=18)
    rule(d, 664)

    # row 3: summit, Fiji, Korea
    row3_y = 672
    col_w = 304
    cols = [
        (36, flags_icon, "DIPLOMACY  •  APEC, SHENZHEN",
         "Trump, Xi and Putin in first three-way talks",
         "The three leaders meet to discuss nuclear risks and "
         "energy security."),
        (360, drought_icon, "PACIFIC  •  FIJI",
         "Fiji declares disaster as drought bites",
         "El Niño has left taps dry across the islands as a "
         "state of disaster is declared."),
        (684, court_icon, "SOUTH KOREA  •  SEOUL",
         "Court clears ex-PM Han Duck-soo",
         "The Supreme Court overturns the conviction from "
         "the 2024 martial law crisis."),
    ]
    for x, icon, kick, head, body in cols:
        icon(d, (x, row3_y, x + 96, row3_y + 84))
        kicker_head_body(d, x, row3_y + 92, col_w, kick, head, body,
                         head_size=21, body_size=16)
    rule(d, 896)

    # ticker
    d.rounded_rectangle([36, 916, 988, 986], radius=8, fill=NAVY)
    f_tick = font(SANS_B, 18)
    tick1 = "GTA 6 EARNS $1.84BN IN A DAY  •  NICHOLLS 113* LIFTS NEW ZEALAND"
    tick2 = "SENSEX UP 1.2%  •  WORLD CHILDREN'S DAY"
    for i, line in enumerate((tick1, tick2)):
        lw = d.textlength(line, font=f_tick)
        d.text(((W - lw) / 2, 926 + i * 26), line, font=f_tick,
               fill=(245, 245, 245))
    f_foot = font(SANS, 13)
    foot = "THE WORLD IN ONE DAY  •  20 NOVEMBER 2026  •  make.fun"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 998), foot, font=f_foot, fill=(90, 90, 90))

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
