from PIL import Image, ImageDraw
import os

# Renderiza em alta resolução (supersampling) e reduz para suavizar
S = 1024
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

# --- Fundo com degradê vertical (indigo -> violeta) ---
grad = Image.new("RGBA", (S, S))
top = (79, 70, 229)      # #4f46e5
bot = (124, 58, 237)     # #7c3aed
for y in range(S):
    t = y / (S - 1)
    r = int(top[0] + (bot[0] - top[0]) * t)
    g = int(top[1] + (bot[1] - top[1]) * t)
    b = int(top[2] + (bot[2] - top[2]) * t)
    for x_line in range(S):
        pass
    grad.paste((r, g, b, 255), (0, y, S, y + 1))

# --- Máscara de cantos arredondados ---
mask = Image.new("L", (S, S), 0)
md = ImageDraw.Draw(mask)
radius = int(S * 0.22)
margin = int(S * 0.06)
md.rounded_rectangle([margin, margin, S - margin, S - margin], radius=radius, fill=255)
img.paste(grad, (0, 0), mask)

draw = ImageDraw.Draw(img)

# --- Brilho sutil no topo ---
gloss = Image.new("RGBA", (S, S), (0, 0, 0, 0))
gd = ImageDraw.Draw(gloss)
gd.rounded_rectangle([margin, margin, S - margin, int(S * 0.5)],
                     radius=radius, fill=(255, 255, 255, 32))
img = Image.alpha_composite(img, Image.composite(gloss, Image.new("RGBA", (S, S), (0,0,0,0)), mask))
draw = ImageDraw.Draw(img)

# --- Check branco (linha grossa com pontas arredondadas) ---
def thick_line(d, pts, width, fill):
    d.line(pts, fill=fill, width=width, joint="curve")
    r = width // 2
    for (x, y) in pts:
        d.ellipse([x - r, y - r, x + r, y + r], fill=fill)

lw = int(S * 0.085)
check = [(int(S * 0.30), int(S * 0.52)),
         (int(S * 0.45), int(S * 0.66)),
         (int(S * 0.72), int(S * 0.36))]
# sombra leve do check
thick_line(draw, [(x + int(S*0.008), y + int(S*0.012)) for (x, y) in check],
           lw, (60, 40, 140, 90))
# check branco
thick_line(draw, check, lw, (255, 255, 255, 255))

# --- Exporta PNG e ICO multi-resolução ---
out_dir = os.path.dirname(os.path.abspath(__file__))
png_path = os.path.join(out_dir, "icon.png")
ico_path = os.path.join(out_dir, "icon.ico")

big = img.resize((512, 512), Image.LANCZOS)
big.save(png_path)

sizes = [(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)]
img.resize((256, 256), Image.LANCZOS).save(ico_path, sizes=sizes)

print("Gerado:", ico_path, "e", png_path)
