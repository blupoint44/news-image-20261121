#!/usr/bin/env python3
"""Draw a one-page newspaper for Saturday 21 November 2026.

Pure Python standard library, no network, fully deterministic.
Own raster canvas, own 5x7 bitmap font, own zlib PNG encoder.
Output: $MAKEFUN_OUTPUT_DIR/entry.png  (default /output)
"""
import os, struct, zlib

W, H = 1024, 1024
PAPER = (246, 243, 235)
INK = (18, 18, 18)
RED = (178, 24, 32)
BLUE = (24, 52, 110)
GREY = (92, 92, 92)
LIGHT = (226, 221, 208)
WHITE = (255, 255, 255)

class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))
    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i+3] = bytes(c)
    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            if 0 <= yy < self.h:
                x0, x1 = max(0, x), min(self.w, x + w)
                for xx in range(x0, x1):
                    i = (yy * self.w + xx) * 3
                    self.px[i:i+3] = bytes(c)
    def hline(self, x, y, w, c, t=3):
        self.rect(x, y, w, t, c)
    def vline(self, x, y, h, c, t=3):
        self.rect(x, y, t, h, c)

# 5x7 bitmap font: each glyph is 7 rows of 5 bits, top row first.
_FONT_ROWS = {
 'A':[0x0E,0x11,0x11,0x1F,0x11,0x11,0x11],'B':[0x1E,0x11,0x11,0x1E,0x11,0x11,0x1E],
 'C':[0x0E,0x11,0x10,0x10,0x10,0x11,0x0E],'D':[0x1C,0x12,0x11,0x11,0x11,0x12,0x1C],
 'E':[0x1F,0x10,0x10,0x1E,0x10,0x10,0x1F],'F':[0x1F,0x10,0x10,0x1E,0x10,0x10,0x10],
 'G':[0x0E,0x11,0x10,0x17,0x11,0x11,0x0F],'H':[0x11,0x11,0x11,0x1F,0x11,0x11,0x11],
 'I':[0x0E,0x04,0x04,0x04,0x04,0x04,0x0E],'J':[0x07,0x02,0x02,0x02,0x02,0x12,0x0C],
 'K':[0x11,0x12,0x14,0x18,0x14,0x12,0x11],'L':[0x10,0x10,0x10,0x10,0x10,0x10,0x1F],
 'M':[0x11,0x1B,0x15,0x15,0x11,0x11,0x11],'N':[0x11,0x19,0x15,0x13,0x11,0x11,0x11],
 'O':[0x0E,0x11,0x11,0x11,0x11,0x11,0x0E],'P':[0x1E,0x11,0x11,0x1E,0x10,0x10,0x10],
 'Q':[0x0E,0x11,0x11,0x11,0x15,0x12,0x0D],'R':[0x1E,0x11,0x11,0x1E,0x14,0x12,0x11],
 'S':[0x0F,0x10,0x10,0x0E,0x01,0x01,0x1E],'T':[0x1F,0x04,0x04,0x04,0x04,0x04,0x04],
 'U':[0x11,0x11,0x11,0x11,0x11,0x11,0x0E],'V':[0x11,0x11,0x11,0x11,0x11,0x0A,0x04],
 'W':[0x11,0x11,0x11,0x15,0x15,0x1B,0x11],'X':[0x11,0x0A,0x04,0x04,0x04,0x0A,0x11],
 'Y':[0x11,0x0A,0x04,0x04,0x04,0x04,0x04],'Z':[0x1F,0x01,0x02,0x04,0x08,0x10,0x1F],
 '0':[0x0E,0x11,0x13,0x15,0x19,0x11,0x0E],'1':[0x04,0x0C,0x04,0x04,0x04,0x04,0x0E],
 '2':[0x0E,0x11,0x01,0x02,0x04,0x08,0x1F],'3':[0x1F,0x02,0x04,0x02,0x01,0x11,0x0E],
 '4':[0x02,0x06,0x0A,0x12,0x1F,0x02,0x02],'5':[0x1F,0x10,0x1E,0x01,0x01,0x11,0x0E],
 '6':[0x06,0x08,0x10,0x1E,0x11,0x11,0x0E],'7':[0x1F,0x01,0x02,0x04,0x08,0x08,0x08],
 '8':[0x0E,0x11,0x11,0x0E,0x11,0x11,0x0E],'9':[0x0E,0x11,0x11,0x0F,0x01,0x02,0x0C],
 ' ':[0,0,0,0,0,0,0],'.':[0,0,0,0,0,0x0C,0x0C],',':[0,0,0,0,0x0C,0x04,0x08],
 "'":[0x04,0x04,0x08,0,0,0,0],'-':[0,0,0,0x1F,0,0,0],':':[0,0x0C,0x0C,0,0x0C,0x0C,0],
 '!':[0x04,0x04,0x04,0x04,0x04,0,0x04],'?':[0x0E,0x11,0x01,0x02,0x04,0,0x04],
 '/':[0x01,0x01,0x02,0x04,0x08,0x10,0x10],'&':[0x0C,0x12,0x14,0x08,0x15,0x12,0x0D],
 '(':[0x02,0x04,0x08,0x08,0x08,0x04,0x02],')':[0x08,0x04,0x02,0x02,0x02,0x04,0x08],
 '+':[0,0x04,0x04,0x1F,0x04,0x04,0],'%':[0x18,0x19,0x02,0x04,0x08,0x13,0x03],
 '$':[0x04,0x0F,0x14,0x0E,0x05,0x1E,0x04],';':[0,0x0C,0x0C,0,0x0C,0x04,0x08],
}

def text_w(s, scale):
    return len(s) * 6 * scale - scale

def draw_text(cv, x, y, s, scale, colour, bold=False):
    cx = x
    for ch in s.upper():
        rows = _FONT_ROWS.get(ch, _FONT_ROWS[' '])
        for r in range(7):
            bits = rows[r]
            for cidx in range(5):
                if bits & (1 << (4 - cidx)):
                    cv.rect(cx + cidx * scale, y + r * scale, scale, scale, colour)
                    if bold:
                        cv.rect(cx + cidx * scale + 1, y + r * scale, scale, scale, colour)
        cx += 6 * scale
    return cx

def wrap(s, scale, max_w):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if text_w(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur); cur = wd
    if cur:
        lines.append(cur)
    return lines

def draw_block(cv, x, y, s, scale, colour, max_w, leading=None, bold=False):
    leading = leading or (9 * scale)
    for ln in wrap(s, scale, max_w):
        draw_text(cv, x, y, ln, scale, colour, bold)
        y += leading
    return y

def write_png(cv, path):
    raw = b""
    stride = cv.w * 3
    for yy in range(cv.h):
        raw += b"\x00" + bytes(cv.px[yy * stride:(yy + 1) * stride])
    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        return out + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)

def centred(cv, y, s, scale, colour, bold=False):
    draw_text(cv, (W - text_w(s, scale)) // 2, y, s, scale, colour, bold)
    return y + 9 * scale

def panel(cv, x, y, w, kicker, headline, body, accent):
    cv.rect(x, y, w, 6, accent)
    draw_text(cv, x, y + 12, kicker, 2, accent, True)
    y2 = draw_block(cv, x, y + 30, headline, 3, INK, w, 27, True)
    y3 = draw_block(cv, x, y2 + 3, body, 2, GREY, w, 18)
    return max(y3, y + 112)

def build():
    cv = Canvas(W, H, PAPER)
    cv.rect(0, 0, W, H, PAPER)
    # Masthead
    cv.rect(28, 24, W - 56, 118, INK)
    centred(cv, 42, "THE WORLD IN ONE DAY", 7, WHITE, True)
    centred(cv, 108, "SATURDAY 21 NOVEMBER 2026", 3, (255, 205, 90), True)
    cv.hline(28, 152, W - 56, RED, 6)
    draw_text(cv, 32, 164, "ONE IMAGE - THE WHOLE DAY - NO. 21", 2, GREY)
    draw_text(cv, W - 32 - text_w("PRICE: THE TRUTH", 2), 164, "PRICE: THE TRUTH", 2, GREY)
    # Lead story
    y = 192
    draw_text(cv, 32, y, "WAR IN EUROPE - NATO SOIL", 3, RED, True); y += 30
    y = draw_block(cv, 32, y, "RUSSIAN MISSILE", 8, INK, W - 64, 70, True)
    y = draw_block(cv, 32, y, "HITS POLAND AS", 8, INK, W - 64, 70, True)
    y = draw_block(cv, 32, y, "KYIV BRIDGES STRUCK", 8, RED, W - 64, 70, True)
    y += 4
    y = draw_block(cv, 32, y,
        "PM TUSK CALLS IT A LIKELY DELIBERATE PROVOCATION. A MASS STRIKE HIT THREE KYIV "
        "BRIDGES AND KRYVYI RIH: 2 DEAD, 42 INJURED, FOUR OF THEM CHILDREN.",
        2, INK, W - 64, 19)
    cv.hline(32, y + 4, W - 64, INK, 4)
    y += 18
    # Six panels in two columns, three rows
    col_w = (W - 64 - 24) // 2
    rows_y = y
    for i, (kick, head, body, acc) in enumerate(PANELS):
        px = 32 + (i % 2) * (col_w + 24)
        py = rows_y + (i // 2) * 130
        if i % 2 == 1:
            cv.vline(px - 14, py, 112, LIGHT, 3)
        panel(cv, px, py, col_w, kick, head, body, acc)
    y = rows_y + 3 * 130 + 4
    # Also-today strip
    cv.rect(28, y, W - 56, 96, BLUE)
    draw_text(cv, 44, y + 10, "ALSO TODAY", 3, (255, 205, 90), True)
    yy = y + 40
    for ln in ALSO:
        draw_text(cv, 44, yy, ln, 2, WHITE)
        yy += 19
    # Footer
    fy = y + 104
    cv.hline(32, fy, W - 64, INK, 3)
    draw_text(cv, 32, fy + 10,
              "SOURCES: BBC - REUTERS - AP - AL JAZEERA - UKMTO - 21 NOV 2026", 2, GREY)
    return cv

PANELS = [
    ("BREXIT RESET - LONDON / BRUSSELS", "UK AND EU STRIKE LANDMARK DEAL TO REBUILD TIES",
     "FOOD, EMISSIONS, YOUTH SCHEME. PM: EXPLORE CLOSER TIES.", BLUE),
    ("DIPLOMACY - SHENZHEN", "TRUMP, XI AND PUTIN ISSUE JOINT PEACE DECLARATION",
     "LEADERS PLEDGE PEACE. KUSHNER: RUSSIA EASES ON UKRAINE.", RED),
    ("WORLD COURT - THE HAGUE", "MYANMAR GENOCIDE VERDICT: ROHINGYA REJOICE",
     "ROHINGYA WELCOME ICJ RULING. UK EXPELS MYANMAR DIPLOMAT.", BLUE),
    ("MARKETS - GLOBAL", "TECH SELL-OFF DEEPENS AS ANTHROPIC SHARES SLIDE",
     "AI STOCKS DRAG MARKETS. ASIA: WORST WEEK SINCE 2020.", RED),
    ("SECURITY - COPENHAGEN", "DENMARK FOILS ALLEGED RUSSIAN ASSASSINATION PLOT",
     "RUSSIAN DIPLOMAT EXPELLED OVER PLOT TO KILL A RAPPER.", BLUE),
    ("SCIENCE - ARTIFICIAL INTELLIGENCE", "ANTHROPIC AI MAY HAVE SOLVED RIEMANN HYPOTHESIS",
     "AI MAY HAVE SOLVED MATHS' BIGGEST OPEN PROBLEM.", RED),
]

ALSO = [
    "- TANKER ABLAZE IN STRAIT OF HORMUZ AFTER PROJECTILE HIT NEAR OMAN",
    "- TRUMP THREATENS BAN ON US FIRMS BUILDING AI DATA CENTRES OVERSEAS",
    "- MAMDANI UNVEILS PLAN TO CLOSE NEW YORK'S RIKERS ISLAND JAIL BY 2032",
]

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    write_png(build(), os.path.join(out_dir, "entry.png"))

if __name__ == "__main__":
    main()


