"""Text cover for 'Big Tech Spent More Than It Earned on AI This Quarter. I Did the Payback Math.'
Drawn with code (numpy + Pillow), no AI image generation. Numbers from the article's own calculations."""
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

R = json.load(open("../results/results.json"))
Wp, Hp = 2880, 1620
F = "/usr/share/fonts/opentype/inter/"
fnt = lambda n, s: ImageFont.truetype(F + n, s)
ORANGE, BLUE, GREEN, GREY, ICE = (255, 140, 66), (90, 170, 255), (63, 185, 120), (200, 206, 216), (160, 220, 255)

yy, xx = np.mgrid[0:Hp, 0:Wp] / np.array([Hp, Wp])[:, None, None]
bg = np.zeros((Hp, Wp, 3)); bg[..., 0] = 9 + 6 * xx; bg[..., 1] = 11 + 6 * xx; bg[..., 2] = 20 + 10 * xx
img = Image.fromarray(bg.clip(0, 255).astype("uint8")).convert("RGBA")
d = ImageDraw.Draw(img)

# right: quarterly capex bars (Epoch 2022-2025 + Q3 2026), rising
tot = [sum(R["hist"][c][i] for c in R["hist"]) for i in range(len(R["quarters"]))]
q3 = R["q3"]; tot.append(q3["Microsoft"]["capex_incl_leases"] + q3["Amazon"]["capex"] + q3["Alphabet"]["capex"] + q3["Meta"]["capex"])
bx, by, bw, gap, sc = 1700, 1380, 40, 14, 5.0
for i, v in enumerate(tot):
    x0 = bx + i * (bw + gap) + (60 if i == len(tot) - 1 else 0)
    col = ORANGE if i == len(tot) - 1 else (90, 110, 140)
    d.rounded_rectangle((x0, by - v * sc, x0 + bw, by), radius=6, fill=col)
d.text((bx, by + 26), "2022", font=fnt("Inter-Medium.otf", 30), fill=GREY)
d.text((bx + 16 * (bw + gap) + 60 + bw, by + 26), "Q3 2026", font=fnt("Inter-Medium.otf", 30), fill=ORANGE, anchor="ra")
d.text((bx + 16 * (bw + gap) + 60 + bw / 2, by - tot[-1] * sc - 20), f"${tot[-1]:.0f}B", font=fnt("Inter-Bold.otf", 40), fill="white", anchor="mb")
d.text((bx, by - tot[-1] * sc - 20), "Capex per quarter,\n4 companies", font=fnt("Inter-Medium.otf", 30), fill=GREY, anchor="ld")

X = 170
d.text((X, 200), "AI ECONOMICS  ·  A REAL EXPERIMENT", font=fnt("Inter-SemiBold.otf", 40), fill=ICE)
big = fnt("InterDisplay-ExtraBold.otf", 108)
for i, line in enumerate(("Big Tech spent more", "than it earned on AI", "this quarter.")):
    d.text((X, 275 + i * 128), line, font=big, fill="white")
d.text((X, 690), "I did the payback math.", font=fnt("Inter-SemiBold.otf", 66), fill=ORANGE)
for j, (num, l1, l2, col) in enumerate(((f"${R['req_cum']:.0f}B", "a year needed to pay back", "the 2024–26 build-out", ORANGE),
                                        (f"${R['new_total']:.0f}B", "of new revenue a year", "so far (Q3 2026 pace)", GREEN))):
    cx = X + j * 830
    d.rounded_rectangle((cx, 840, cx + 790, 1000), radius=24, outline=col, width=3, fill=(18, 24, 36, 255))
    d.text((cx + 30, 866), num, font=fnt("Inter-ExtraBold.otf", 80), fill=col)
    d.text((cx + 330, 876), l1, font=fnt("Inter-Medium.otf", 32), fill="white")
    d.text((cx + 330, 918), l2, font=fnt("Inter-Medium.otf", 32), fill=GREY)
d.text((X, 1070), "Alphabet · Amazon · Meta · Microsoft  ·  earnings week, Oct 2026", font=fnt("Inter-Medium.otf", 36), fill=GREY)
img.convert("RGB").save("cover_ai_capex.png", optimize=True)
img.convert("RGB").resize((1400, 788), Image.LANCZOS).save("cover_ai_capex_medium.png", optimize=True)
print("ok")
