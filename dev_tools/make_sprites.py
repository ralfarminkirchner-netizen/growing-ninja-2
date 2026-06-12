#!/usr/bin/env python3
"""Erzeugt alle Pixel-Art-Platzhalter-PNGs fuer "Growing Ninja - First Steps".

Aufruf:  python3 make_sprites.py
Schreibt nach: ../assets/sprites/

Die Sprites sind bewusst einfache Platzhalter - spaeter durch echte
Pixel-Art (z. B. Kenney-Assets oder eigene Aseprite-Sprites) ersetzen.
"""
import math
import os
import random

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "assets", "sprites"))
os.makedirs(OUT, exist_ok=True)
random.seed(20260612)

# ---------- Palette (sanft, kinderfreundlich) ----------
HOOD = (124, 92, 191, 255)      # Lila Kapuze
HOOD_D = (84, 60, 138, 255)
BODY = (95, 120, 220, 255)      # Blaues Gewand
BODY_D = (60, 78, 160, 255)
BELT = (255, 158, 66, 255)      # Oranger Guertel
SCARF = (255, 132, 64, 255)     # Oranger Schal
FACE = (255, 219, 182, 255)
EYE = (40, 32, 66, 255)
BAND = (95, 156, 232, 255)      # Blaues Stirnband
WHITE = (255, 255, 255, 255)


def save(img, name):
    img.save(os.path.join(OUT, name))
    print("ok", name, img.size)


# =====================================================================
# Ninja-Spritesheet: 6 Spalten x 5 Reihen a 32x32
#   Reihe 0: Idle (4)   Reihe 1: Run (6)   Reihe 2: Jump (2)
#   Reihe 3: Fall (2)   Reihe 4: Land (3)
# =====================================================================
def draw_ninja(d, ox, oy, bob=0, legs=("stand", 0), scarf=0, squash=0):
    oy += bob + squash
    ly = oy + 26 - squash  # Beinhoehe (Fuesse bleiben fix bei y=30)
    mode, ph = legs
    if mode == "stand":
        d.rectangle([ox + 13, ly, ox + 14, ly + 4], fill=BODY_D)
        d.rectangle([ox + 17, ly, ox + 18, ly + 4], fill=BODY_D)
    elif mode == "run":
        seq = [(-2, 0), (-1, -1), (0, 0), (2, 0), (1, -1), (0, 0)]
        fx, fy = seq[ph % 6]
        bx, by = seq[(ph + 3) % 6]
        d.rectangle([ox + 13 + fx, ly + fy, ox + 14 + fx, ly + 4 + fy], fill=BODY_D)
        d.rectangle([ox + 17 + bx, ly + by, ox + 18 + bx, ly + 4 + by], fill=BODY_D)
    elif mode == "tuck":  # Sprung: Beine angezogen
        d.rectangle([ox + 13, ly, ox + 14, ly + 2], fill=BODY_D)
        d.rectangle([ox + 17, ly, ox + 18, ly + 2], fill=BODY_D)
    elif mode == "spread":  # Fall: Beine gespreizt
        d.rectangle([ox + 11, ly, ox + 12, ly + 3], fill=BODY_D)
        d.rectangle([ox + 19, ly, ox + 20, ly + 3], fill=BODY_D)
    # Koerper + Guertel
    d.rectangle([ox + 12, oy + 19, ox + 19, oy + 26 - squash], fill=BODY)
    d.rectangle([ox + 12, oy + 22, ox + 19, oy + 23], fill=BELT)
    # Kapuze (grosser, niedlicher Kopf)
    d.rectangle([ox + 9, oy + 6, ox + 22, oy + 18], fill=HOOD)
    d.rectangle([ox + 10, oy + 5, ox + 21, oy + 5], fill=HOOD)
    d.rectangle([ox + 8, oy + 8, ox + 8, oy + 16], fill=HOOD)
    d.rectangle([ox + 23, oy + 8, ox + 23, oy + 16], fill=HOOD)
    d.rectangle([ox + 9, oy + 17, ox + 22, oy + 18], fill=HOOD_D)
    # Gesicht + grosse Augen
    d.rectangle([ox + 11, oy + 10, ox + 20, oy + 14], fill=FACE)
    d.rectangle([ox + 13, oy + 11, ox + 14, oy + 13], fill=EYE)
    d.rectangle([ox + 18, oy + 11, ox + 19, oy + 13], fill=EYE)
    d.point((ox + 13, oy + 11), fill=WHITE)
    d.point((ox + 18, oy + 11), fill=WHITE)
    # Stirnband
    d.rectangle([ox + 8, oy + 8, ox + 23, oy + 9], fill=BAND)
    # Schal-Zipfel, flattert je nach Frame
    tails = [
        [(24, 9), (25, 10), (26, 10)],
        [(24, 9), (25, 9), (26, 8)],
        [(24, 10), (25, 11), (26, 12)],
        [(24, 8), (25, 7), (26, 7)],
    ]
    for tx, ty in tails[scarf % 4]:
        d.point((ox + tx, oy + ty), fill=SCARF)
        d.point((ox + tx, oy + ty + 1), fill=SCARF)


sheet = Image.new("RGBA", (6 * 32, 5 * 32), (0, 0, 0, 0))
d = ImageDraw.Draw(sheet)
# Reihe 0: Idle (atmet leicht)
for i, bob in enumerate([0, 0, 1, 1]):
    draw_ninja(d, i * 32, 0, bob=bob, legs=("stand", 0), scarf=i % 2)
# Reihe 1: Run
for i in range(6):
    draw_ninja(d, i * 32, 32, bob=[0, 1, 0, 0, 1, 0][i], legs=("run", i), scarf=2 if i % 2 else 0)
# Reihe 2: Jump (mit wehendem Schal)
for i in range(2):
    draw_ninja(d, i * 32, 64, bob=-1, legs=("tuck", 0), scarf=3 if i == 0 else 1)
# Reihe 3: Fall
for i in range(2):
    draw_ninja(d, i * 32, 96, bob=0, legs=("spread", 0), scarf=2 if i == 0 else 0)
# Reihe 4: Land (Squash)
for i, sq in enumerate([3, 2, 0]):
    draw_ninja(d, i * 32, 128, bob=0, legs=("stand", 0), scarf=2, squash=sq)
save(sheet, "ninja_sheet.png")

# =====================================================================
# Weisheits-Stern 16x16 (gelb mit Glow)
# =====================================================================
star = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
d = ImageDraw.Draw(star)
d.ellipse([1, 1, 14, 14], fill=(255, 230, 120, 55))
d.ellipse([3, 3, 12, 12], fill=(255, 235, 140, 90))
pts = []
for k in range(10):
    ang = -math.pi / 2 + k * math.pi / 5
    r = 7 if k % 2 == 0 else 3
    pts.append((7.5 + r * math.cos(ang), 7.5 + r * math.sin(ang)))
d.polygon(pts, fill=(255, 224, 92, 255))
d.rectangle([7, 7, 8, 8], fill=WHITE)
save(star, "star.png")

# =====================================================================
# Tile-Atlas 160x32: 5 Tiles a 32x32
#   0 Boden oben | 1 Boden innen | 2 Wolke | 3 Pilz | 4 Kristallblock
# =====================================================================
tiles = Image.new("RGBA", (160, 32), (0, 0, 0, 0))
d = ImageDraw.Draw(tiles)
# Tile 0: Boden mit leuchtendem Nacht-Gras
d.rectangle([0, 0, 31, 31], fill=(46, 39, 80, 255))
d.rectangle([0, 0, 31, 5], fill=(63, 174, 140, 255))
d.rectangle([0, 6, 31, 7], fill=(43, 122, 104, 255))
for _ in range(6):
    d.point((random.randint(0, 31), random.randint(0, 4)), fill=(180, 255, 220, 255))
for _ in range(8):
    d.point((random.randint(0, 31), random.randint(10, 31)), fill=(36, 29, 64, 255))
# Tile 1: Boden innen
d.rectangle([32, 0, 63, 31], fill=(46, 39, 80, 255))
for _ in range(14):
    d.point((random.randint(32, 63), random.randint(0, 31)), fill=(36, 29, 64, 255))
for _ in range(5):
    d.point((random.randint(32, 63), random.randint(0, 31)), fill=(58, 50, 98, 255))
# Tile 2: Wolken-Plattform
d.ellipse([65, 2, 94, 20], fill=(232, 242, 255, 255))
d.ellipse([68, 8, 80, 22], fill=(232, 242, 255, 255))
d.ellipse([80, 8, 92, 22], fill=(232, 242, 255, 255))
d.ellipse([70, 17, 90, 23], fill=(200, 216, 245, 255))
# Tile 3: Pilz-Plattform
d.rectangle([109, 12, 114, 31], fill=(242, 230, 216, 255))
d.ellipse([97, 0, 126, 15], fill=(224, 96, 122, 255))
d.ellipse([102, 3, 107, 8], fill=(255, 210, 220, 255))
d.ellipse([114, 5, 119, 10], fill=(255, 210, 220, 255))
d.rectangle([97, 13, 126, 14], fill=(180, 70, 95, 255))
# Tile 4: Leuchtender Kristallblock
d.rectangle([128, 0, 159, 31], fill=(24, 40, 66, 255))
d.polygon([(143, 2), (154, 16), (143, 30), (133, 16)], fill=(95, 215, 232, 255))
d.polygon([(143, 2), (148, 16), (143, 30), (139, 16)], fill=(160, 240, 250, 255))
d.point((143, 8), fill=WHITE)
save(tiles, "tiles.png")

# =====================================================================
# Leuchtendes Ziel-Tor 48x64
# =====================================================================
portal = Image.new("RGBA", (48, 64), (0, 0, 0, 0))
d = ImageDraw.Draw(portal)
d.pieslice([4, 4, 43, 43], 180, 360, fill=(211, 107, 255, 255))
d.rectangle([4, 24, 43, 63], fill=(211, 107, 255, 255))
d.pieslice([9, 9, 38, 38], 180, 360, fill=(150, 235, 255, 235))
d.rectangle([9, 24, 38, 63], fill=(150, 235, 255, 235))
d.pieslice([15, 15, 32, 32], 180, 360, fill=(225, 250, 255, 245))
d.rectangle([15, 24, 32, 63], fill=(225, 250, 255, 245))
d.rectangle([0, 60, 47, 63], fill=(84, 60, 138, 255))
for _ in range(10):
    d.point((random.randint(12, 35), random.randint(16, 56)), fill=WHITE)
save(portal, "portal.png")

# =====================================================================
# Checkpoint-Kristall 32x32
# =====================================================================
cp = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
d = ImageDraw.Draw(cp)
d.rectangle([8, 28, 24, 31], fill=(60, 50, 98, 255))
d.polygon([(16, 2), (24, 18), (16, 29), (8, 18)], fill=(120, 225, 210, 255))
d.polygon([(16, 2), (19, 18), (16, 29), (13, 18)], fill=(190, 250, 240, 255))
d.point((16, 8), fill=WHITE)
save(cp, "checkpoint.png")

# =====================================================================
# Parallax-Hintergrund fern: 640x360, Nachthimmel mit Sternen
# =====================================================================
bg = Image.new("RGBA", (640, 360), (0, 0, 0, 255))
d = ImageDraw.Draw(bg)
for y in range(360):
    t = y / 359.0
    col = (int(8 + 12 * t), int(11 + 15 * t), int(38 + 23 * t), 255)
    d.line([(0, y), (639, y)], fill=col)
for _ in range(160):
    x, y = random.randint(0, 639), random.randint(0, 359)
    c = random.choice([(255, 255, 255), (255, 240, 200), (190, 210, 255)])
    a = random.randint(110, 255)
    d.point((x, y), fill=c + (a,))
for _ in range(18):
    x, y = random.randint(0, 638), random.randint(0, 358)
    d.rectangle([x, y, x + 1, y + 1], fill=(255, 252, 230, 255))
save(bg, "bg_far.png")

# =====================================================================
# Parallax-Hintergrund nah: 640x480, Mond + grosse Funkelsterne
# =====================================================================
ng = Image.new("RGBA", (640, 480), (0, 0, 0, 0))
d = ImageDraw.Draw(ng)
d.ellipse([466, 26, 554, 114], fill=(255, 247, 217, 40))
d.ellipse([476, 36, 544, 104], fill=(255, 247, 217, 70))
d.ellipse([486, 46, 534, 94], fill=(255, 247, 217, 255))
d.ellipse([498, 58, 508, 68], fill=(235, 222, 185, 255))
d.ellipse([516, 76, 523, 83], fill=(235, 222, 185, 255))
for _ in range(30):
    x, y = random.randint(4, 635), random.randint(4, 420)
    d.rectangle([x, y, x + 1, y + 1], fill=(255, 250, 230, 200))
    d.point((x - 1, y), fill=(255, 250, 230, 110))
    d.point((x + 2, y), fill=(255, 250, 230, 110))
    d.point((x, y - 1), fill=(255, 250, 230, 110))
    d.point((x, y + 2), fill=(255, 250, 230, 110))
for cx, cy in [(120, 430), (360, 455), (560, 440)]:
    d.ellipse([cx - 70, cy - 16, cx + 70, cy + 16], fill=(26, 32, 72, 150))
    d.ellipse([cx - 40, cy - 26, cx + 40, cy + 6], fill=(26, 32, 72, 150))
save(ng, "bg_near.png")

print("Alle Sprites erzeugt ->", OUT)
