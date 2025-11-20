import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from dobble_gen.config import Config
from dobble_gen.symbol import Symbol
from dobble_gen.card import Card


def load_symbols(image_dir: str) -> list[Symbol]:
    """Load and process all valid image files from the specified directory.

    Each image is converted to RGBA, cropped into a circle, and added to the symbols list.
    Unsupported formats or corrupted files are skipped with an error message.

    Args:
        image_dir: Directory containing the image files.

    Returns:
        A list of Symbol objects ready for use in card generation.
    """
    symbols = []
    for f in os.listdir(image_dir):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".heif")):
            path = os.path.join(image_dir, f)
            try:
                s = Symbol(path)
                s.crop_circle()  # Convert image to circular shape
                symbols.append(s)
            except Exception:
                print(f"Error loading image: {path}")
    return symbols


def dobble_combinations(symbol_per_card: int, total_cards: int) -> list[list[int]]:
    """Generate perfect Dobble combinations using finite projective plane theory.

    This algorithm generates a mathematical set of card combinations where:
    - Each card has exactly symbol_per_card symbols
    - Each pair of cards shares exactly one symbol
    - Total cards = n^2 - n + 1 (where n = symbol_per_card - 1)
    - Total unique symbols = n^2 - n + 1

    Args:
        symbol_per_card: Number of symbols per card (must be prime + 1).
        total_cards: Total number of cards to generate.

    Returns:
        A list of combinations, where each combination is a list of symbol IDs (1-indexed).
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


def generate_pdf(output_dir: str, card_dir: str, card_diameter: int) -> None:
    """Assemble individual card images into a print-ready PDF document.

    Cards are arranged on A4 pages in a grid layout with proper spacing.
    Each page is designed to maximize the number of cards while maintaining
    printable margins.

    Args:
        output_dir: Directory where the PDF will be saved.
        card_dir: Directory containing the individual card PNG images.
    """
    pdf_path = os.path.join(output_dir, "dobble.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    page_w, page_h = A4
    cm = 72 / 2.54  # Conversion factor from cm to points (1/72 inch)
    margin = 1.5 * cm
    x, y = margin, page_h - (card_diameter + 2) * cm  # Start position for first card

    for f in sorted(os.listdir(card_dir)):
        if not f.endswith(".png"):
            continue
        path = os.path.join(card_dir, f)
        # Draw card at current position
        c.drawImage(path, x, y, width=card_diameter * cm, height=card_diameter * cm)
        # Move to next position (right)
        x += (card_diameter + 1) * cm
        # Check if we need to move to next row
        if x + (card_diameter + 1) * cm > page_w:
            x = margin
            y -= (card_diameter + 1) * cm
        # Check if we need a new page
        if y < margin:
            c.showPage()
            x, y = margin, page_h - (card_diameter + 2) * cm
    c.save()


def run(config: Config) -> None:
    """Execute the complete Dobble card generation pipeline.

    This is the main orchestration function that:
    1. Loads and processes images from the specified directory
    2. Generates mathematically perfect Dobble combinations
    3. Creates individual card images with properly placed symbols
    4. Assembles all cards into a print-ready PDF

    Args:
        config: Configuration object with all generation parameters.

    Raises:
        SystemExit: If there are not enough unique images for the card set.
        RuntimeError: If card generation fails (symbol count mismatch).
    """
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
        # Map symbol IDs to Symbol objects
        symbol_images = {c: images[c - 1].copy() for c in combo}
        if len(symbol_images) != config.symbols_per_card:
            raise RuntimeError(
                f"Card {i} has {len(symbol_images)} symbols instead of {config.symbols_per_card}."
            )
        # Create and populate card
        card = Card(config.card_diameter_px, symbol_images, filename)
        card.place_cards()
        card.save()
    print("Generating PDF...")
    generate_pdf(config.output_dir, config.card_dir, config.card_diameter_cm)
    print(f"✅ Done! The cards are ready in '{config.output_dir}' 🎴")
