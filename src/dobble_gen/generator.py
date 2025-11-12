import os
import math
import random
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# === PARAMÈTRES ===
CARD_DIAMETER_CM = 8
SYMBOLS_PER_CARD = 7
NUM_CARDS = SYMBOLS_PER_CARD**2 - SYMBOLS_PER_CARD + 1  # = 31
DPI = 300  # qualité impression
CARD_DIAMETER_PX = int(CARD_DIAMETER_CM / 2.54 * DPI)
IMAGE_DIR = "images"
OUTPUT_DIR = "output"
CARD_DIR = os.path.join(OUTPUT_DIR, "cartes")
os.makedirs(CARD_DIR, exist_ok=True)


# === UTILITAIRES ===
def crop_circle(im):
    """Recadre une image en rond."""
    im = im.convert("RGBA")
    mask = Image.new("L", im.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, im.size[0], im.size[1]), fill=255)
    im.putalpha(mask)
    return im


def load_images():
    imgs = []
    for f in sorted(os.listdir(IMAGE_DIR)):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".heif")):
            path = os.path.join(IMAGE_DIR, f)
            try:
                img = Image.open(path).convert("RGBA")
                imgs.append(crop_circle(img))
            except Exception as e:
                print(f"Erreur sur {f}: {e}")
    return imgs


def dobble_combinations(n):
    """Génère les combinaisons Dobble parfaites (plan projectif d'ordre n-1)."""
    order = n - 1
    cards = []
    for i in range(order + 1):
        card = [0]
        for j in range(order):
            card.append(1 + order * i + j + 1)
        cards.append(card)
    for a in range(order):
        for b in range(order):
            card = [a + 1]
            for k in range(order):
                card.append(order + 2 + order * k + ((a * k + b) % order))
            cards.append(card)
    return cards


def no_overlap(x, y, r, placed):
    """Vérifie qu'une image (centre x,y rayon r) ne chevauche pas les autres."""
    for px, py, pr in placed:
        dist = math.hypot(px - x, py - y)
        if dist < (r + pr) * 1.05:  # petite marge pour éviter les collisions
            return False
    return True


def draw_card(symbol_images, indices, filename):
    """Dessine une carte Dobble circulaire avec bordure visible et chaos contrôlé."""
    card = Image.new("RGBA", (CARD_DIAMETER_PX, CARD_DIAMETER_PX), (255, 255, 255, 0))
    draw = ImageDraw.Draw(card)

    # === Cercle de découpe (bordure visible) ===
    border_color = (50, 50, 50, 255)  # gris foncé
    border_width = max(2, CARD_DIAMETER_PX // 200)
    draw.ellipse(
        (
            border_width // 2,
            border_width // 2,
            CARD_DIAMETER_PX - border_width // 2,
            CARD_DIAMETER_PX - border_width // 2,
        ),
        fill=(255, 255, 255, 255),
        outline=border_color,
        width=border_width,
    )

    cx, cy = CARD_DIAMETER_PX // 2, CARD_DIAMETER_PX // 2
    placed = []
    indices = indices.copy()
    random.shuffle(indices)

    # === Une image centrale (optionnelle) ===
    if random.random() < 0.6:
        idx_center = indices.pop()
        img = symbol_images[idx_center % len(symbol_images)].copy()
        size = int(CARD_DIAMETER_PX * random.uniform(0.18, 0.22))
        img = img.resize((size, size), Image.LANCZOS)
        img = img.rotate(random.uniform(0, 360), expand=True)
        x = cx - img.width // 2
        y = cy - img.height // 2
        card.alpha_composite(img, (x, y))
        placed.append((cx, cy, size / 2))

    # === Autres symboles sans chevauchement ===
    for idx in indices:
        img = symbol_images[idx % len(symbol_images)].copy()
        size = int(CARD_DIAMETER_PX * random.uniform(0.15, 0.25))
        img = img.resize((size, size), Image.LANCZOS)
        img = img.rotate(random.uniform(0, 360), expand=True)

        for _ in range(250):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(0.15, 0.42) * CARD_DIAMETER_PX
            x = int(cx + radius * math.cos(angle))
            y = int(cy + radius * math.sin(angle))
            if no_overlap(x, y, size / 2, placed):
                card.alpha_composite(img, (x - img.width // 2, y - img.height // 2))
                placed.append((x, y, size / 2))
                break

    card.save(filename, "PNG")


def generate_pdf():
    """Assemble les cartes dans un PDF A4 avec bordures visibles."""
    pdf_path = os.path.join(OUTPUT_DIR, "dobble.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    page_w, page_h = A4
    cm = 72 / 2.54
    margin = 1.5 * cm
    x, y = margin, page_h - 10 * cm

    for f in sorted(os.listdir(CARD_DIR)):
        if not f.endswith(".png"):
            continue
        path = os.path.join(CARD_DIR, f)
        c.drawImage(path, x, y, width=8 * cm, height=8 * cm)
        x += 9 * cm
        if x + 8 * cm > page_w:
            x = margin
            y -= 9 * cm
        if y < margin:
            c.showPage()
            x, y = margin, page_h - 10 * cm
    c.save()


# === MAIN ===
def main():
    print("Chargement des images…")
    images = load_images()
    if len(images) < NUM_CARDS:
        print(f"⚠️ Il faut {NUM_CARDS} images uniques (tu en as {len(images)}).")
        print("Je vais réutiliser certaines images pour compléter.")
        while len(images) < NUM_CARDS:
            images += images[: NUM_CARDS - len(images)]

    print("Génération des combinaisons Dobble…")
    combos = dobble_combinations(SYMBOLS_PER_CARD)

    print("Création des cartes avec bordure visible…")
    for i, combo in enumerate(combos):
        filename = os.path.join(CARD_DIR, f"carte_{i + 1:02}.png")
        draw_card(images, combo, filename)

    print("Génération du PDF…")
    generate_pdf()
    print("✅ Terminé ! Les cartes sont prêtes dans 'output/' 🎴")
