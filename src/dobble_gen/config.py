from __future__ import annotations

import os

DEFAULT_IMAGES_DIR = "images"
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_SYMBOLS_PER_CARD = 8
DEFAULT_CARD_DIAMETER_CM = 10
DEFAULT_DPI = 300
DEFAULT_MAX_PLACEMENT_RETRIES = 1000


def nb_cards(symbols_per_card: int) -> int:
    return (symbols_per_card**2) - symbols_per_card + 1


class Config:
    def __init__(
        self,
        image_dir: str = DEFAULT_IMAGES_DIR,
        output_dir: str = DEFAULT_OUTPUT_DIR,
        symbols_per_card: int = DEFAULT_SYMBOLS_PER_CARD,
        card_diameter_cm: int = DEFAULT_CARD_DIAMETER_CM,
        max_placement_retries: int = DEFAULT_MAX_PLACEMENT_RETRIES,
        dpi: int = DEFAULT_DPI,
    ):
        self.image_dir = image_dir
        self.output_dir = output_dir
        self.symbols_per_card = symbols_per_card
        self.card_diameter_cm = card_diameter_cm
        self.card_dir = os.path.join(output_dir, "cards")
        self.num_cards = nb_cards(symbols_per_card)
        self.card_diameter_px = int(card_diameter_cm / 2.54 * dpi)
        self.max_placement_retries = max_placement_retries
        self.dpi = dpi

    def create_output_dir(self) -> None:
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.card_dir, exist_ok=True)
