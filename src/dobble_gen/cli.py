from __future__ import annotations
import sys

import typer
from rich import print
from dobble_gen import check, generator
from dobble_gen.config import (
    Config,
    DEFAULT_IMAGES_DIR,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SYMBOLS_PER_CARD,
    DEFAULT_CARD_DIAMETER_CM,
    DEFAULT_DPI,
    DEFAULT_MAX_PLACEMENT_RETRIES,
)

app = typer.Typer()


@app.command()
def run(
    images_dir: str = DEFAULT_IMAGES_DIR,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    symbols_per_card: int = DEFAULT_SYMBOLS_PER_CARD,
    card_diameter_cm: int = DEFAULT_CARD_DIAMETER_CM,
    max_placement_retries: int = DEFAULT_MAX_PLACEMENT_RETRIES,
    dpi: int = DEFAULT_DPI,
) -> None:
    """Generate Dobble cards from images in the specified directory.

    This is the main command that loads images, generates the Dobble
    combinations, creates individual cards, and assembles them into a PDF.

    Args:
        images_dir: Directory containing the image files to use as symbols.
        output_dir: Directory where the output cards and PDF will be saved.
        symbols_per_card: Number of symbols per card (must be prime + 1).
        card_diameter_cm: Diameter of each card in centimeters.
        max_placement_retries: Maximum attempts to place symbols on each card.
        dpi: Resolution of the output images in dots per inch.
    """
    if not check.is_prime(symbols_per_card - 1):
        print("symbol per card must be a prime number +1")
        sys.exit(1)
    cfg = Config(
        images_dir,
        output_dir,
        symbols_per_card,
        card_diameter_cm,
        max_placement_retries,
        dpi,
    )
    generator.run(cfg)


@app.command()
def create_output_dir(
    images_dir: str = DEFAULT_IMAGES_DIR,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> None:
    """Create the output directory structure.

    Args:
        images_dir: Directory containing the image files.
        output_dir: Directory where the output structure will be created.
    """
    cfg = Config(images_dir, output_dir)
    cfg.create_output_dir()
    print(f"{output_dir} directory created.")


def main():
    """Entry point for the CLI application."""
    app()
