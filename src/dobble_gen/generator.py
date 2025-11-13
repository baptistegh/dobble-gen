import os
import math
import random
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from dobble_gen.config import Config


def crop_circle(im):
    """Crop an image into a circle."""
    im = im.convert("RGBA")
    mask = Image.new("L", im.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, im.size[0], im.size[1]), fill=255)
    im.putalpha(mask)
    return im


def load_images(image_dir: str):
    imgs = []
    for f in sorted(os.listdir(image_dir)):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".heif")):
            path = os.path.join(image_dir, f)
            try:
                img = Image.open(path).convert("RGBA")
                imgs.append(crop_circle(img))
            except Exception as e:
                print(f"Erreur sur {f}: {e}")
    return imgs


def dobble_combinations(symbol_per_card: int, total_cards: int) -> list:
    """
    Generate perfect Dobble combinations using a finite projective plane of order n.
    Each card has n+1 symbols, each pair of cards shares exactly one symbol.
    Total symbols = n^2 - n + 1
    Total cards = n^2 - n + 1
    """
    cards: list = []
    n = symbol_per_card - 1
    t = []
    t.append([[(i + 1) + (j * n) for i in range(n)] for j in range(n)])
    for ti in range(n - 1):
        t.append(
            [
                [t[0][((ti + 1) * i) % n][(j + i) % n] for i in range(n)]
                for j in range(n)
            ]
        )
    t.append([[t[0][i][j] for i in range(n)] for j in range(n)])
    for i in range(n):
        t[0][i].append(total_cards - n)
        t[n][i].append(total_cards - n + 1)
        for ti in range(n - 1):
            t[ti + 1][i].append(total_cards - n + 1 + ti + 1)
    t.append([[(i + (total_cards - n)) for i in range(symbol_per_card)]])
    for tv in t:
        cards = cards + tv
    return cards


def no_overlap(x, y, r, placed):
    """Check that an image (center x, y, radius r) does not overlap the others."""
    for px, py, pr in placed:
        dist = math.hypot(px - x, py - y)
        if dist < (r + pr) * 1.05:
            return False
    return True


def draw_card(
    card_diameter_px: int,
    symbol_images: list[Image.Image],
    indices: list[int],
    filename: str,
):
    """Draw a circular Dobble card with all constraints."""
    card = Image.new("RGBA", (card_diameter_px, card_diameter_px), (255, 255, 255, 0))
    draw = ImageDraw.Draw(card)

    # === Cercle de découpe ===
    border_color = (50, 50, 50, 255)
    border_width = max(2, card_diameter_px // 200)
    draw.ellipse(
        (
            border_width // 2,
            border_width // 2,
            card_diameter_px - border_width // 2,
            card_diameter_px - border_width // 2,
        ),
        fill=(255, 255, 255, 255),
        outline=border_color,
        width=border_width,
    )

    cx, cy = card_diameter_px // 2, card_diameter_px // 2
    radius_limit = card_diameter_px / 2 - border_width // 2
    placed = []

    indices = list(dict.fromkeys(indices))  # aucune image répétée
    random.shuffle(indices)

    # Image centrale optionnelle
    if random.random() < 0.6:
        idx_center = indices.pop()
        img = symbol_images[idx_center % len(symbol_images)].copy()
        size = int(card_diameter_px * random.uniform(0.18, 0.22))
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        img = img.rotate(random.uniform(0, 360), expand=True)
        x = cx - img.width // 2
        y = cy - img.height // 2
        card.alpha_composite(img, (x, y))
        placed.append((cx, cy, size / 2))

    # Autres images
    for idx in indices:
        img = symbol_images[idx % len(symbol_images)].copy()
        size = int(card_diameter_px * random.uniform(0.15, 0.25))
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        img = img.rotate(random.uniform(0, 360), expand=True)

        for _ in range(300):
            angle = random.uniform(0, 2 * math.pi)
            max_radius = radius_limit - size / 2
            radius = random.uniform(0, max_radius)
            x = int(cx + radius * math.cos(angle))
            y = int(cy + radius * math.sin(angle))
            if no_overlap(x, y, size / 2, placed):
                card.alpha_composite(img, (x - img.width // 2, y - img.height // 2))
                placed.append((x, y, size / 2))
                break

    card.save(filename, "PNG")


def generate_pdf(output_dir: str, card_dir):
    pdf_path = os.path.join(output_dir, "dobble.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    page_w, page_h = A4
    cm = 72 / 2.54
    margin = 1.5 * cm
    x, y = margin, page_h - 12 * cm

    for f in sorted(os.listdir(card_dir)):
        if not f.endswith(".png"):
            continue
        path = os.path.join(card_dir, f)
        c.drawImage(path, x, y, width=10 * cm, height=10 * cm)
        x += 11 * cm
        if x + 10 * cm > page_w:
            x = margin
            y -= 11 * cm
        if y < margin:
            c.showPage()
            x, y = margin, page_h - 12 * cm
    c.save()


def run(config: Config):
    print("Loading images…")
    images = load_images(config.image_dir)
    if len(images) < config.num_cards:
        print(f"⚠️ You need {config.num_cards} unique images (you have {len(images)}).")
        while len(images) < config.num_cards:
            images += images[: config.num_cards - len(images)]

    print("Generating Dobble combinations...")
    combos = dobble_combinations(config.symbols_per_card, config.num_cards)

    print("Creating cards with constraints...")
    config.create_output_dir()
    for i, combo in enumerate(combos):
        filename = os.path.join(config.card_dir, f"carte_{i + 1:02}.png")
        draw_card(config.card_diameter_px, images, combo, filename)

    print("Generating PDF...")
    generate_pdf(config.output_dir, config.card_dir)
    print(f"✅ Done! The cards are ready in '{config.output_dir}' 🎴")
