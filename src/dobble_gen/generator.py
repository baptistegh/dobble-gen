import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from dobble_gen.config import Config
from dobble_gen.symbol import Symbol
from dobble_gen.card import Card


def load_symbols(image_dir: str) -> list[Symbol]:
    symbols = []
    for f in os.listdir(image_dir):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".heif")):
            path = os.path.join(image_dir, f)
            try:
                s = Symbol(path)
                s.crop_circle()
                symbols.append(s)
            except Exception:
                print(f"Error loading image: {path}")
    return symbols


def dobble_combinations(symbol_per_card: int, total_cards: int) -> list[list[int]]:
    """
    Generate perfect Dobble combinations using a finite projective plane of order n.
    Each card has n+1 symbols, each pair of cards shares exactly one symbol.
    Total symbols = n^2 - n + 1
    Total cards = n^2 - n + 1
    """
    cards: list[list[int]] = []
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
    images = load_symbols(config.image_dir)
    if len(images) < config.num_cards:
        print(f"⚠️ You need {config.num_cards} unique images (you have {len(images)}).")
        sys.exit(1)

    print("Generating Dobble combinations...")
    combos = dobble_combinations(config.symbols_per_card, config.num_cards)

    print("Creating cards with constraints...")
    config.create_output_dir()
    for i, combo in enumerate(combos):
        filename = os.path.join(config.card_dir, f"card_{i}.png")
        symbol_images = {c: images[c - 1].copy() for c in combo}
        if len(symbol_images) != config.symbols_per_card:
            raise RuntimeError(
                f"Card {i} has {len(symbol_images)} symbols instead of {config.symbols_per_card}."
            )
        card = Card(config.card_diameter_px, symbol_images, filename)
        card.place_cards()

        card.save()
    print("Generating PDF...")
    generate_pdf(config.output_dir, config.card_dir)
    print(f"✅ Done! The cards are ready in '{config.output_dir}' 🎴")
