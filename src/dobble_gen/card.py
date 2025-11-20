from PIL import Image, ImageDraw
import math
import random

from dobble_gen.symbol import Symbol

import circlify


class Card:
    """Represents a single Dobble card with symbols arranged in a circle."""

    placed: list[Symbol]

    def __init__(
        self,
        card_diameter_px: int,
        symbol_images: dict[int, Symbol],
        filename: str,
    ):
        """Initialize a Card with the specified dimensions and symbols.

        Args:
            card_diameter_px: The diameter of the card in pixels.
            symbol_images: A dictionary mapping symbol IDs to Symbol objects.
            filename: The output filename for the card PNG image.
        """
        self.card_diameter_px = card_diameter_px
        self.symbol_images = symbol_images
        self.filename = filename
        self.placed = []
        # Create a transparent RGBA image for the card
        self.image = Image.new(
            "RGBA", (card_diameter_px, card_diameter_px), (255, 255, 255, 0)
        )
        self.draw = ImageDraw.Draw(self.image)
        # Set up the card border styling
        self.border_color = (50, 50, 50, 255)
        self.border_width = max(2, self.card_diameter_px // 200)
        # Draw the circular border
        self.draw.ellipse(
            (
                self.border_width // 2,
                self.border_width // 2,
                self.card_diameter_px - self.border_width // 2,
                self.card_diameter_px - self.border_width // 2,
            ),
            fill=(255, 255, 255, 255),
            outline=self.border_color,
            width=self.border_width,
        )

    def place_cards(self) -> None:
        """Arrange all symbols on the card using circle packing algorithm.

        This method uses the circlify algorithm to pack symbols efficiently
        within the card's circular boundary, ensuring no overlaps and random
        rotation angles for visual variety.

        Raises:
            RuntimeError: If not all symbols could be placed on the card.
        """
        available_sizes = [1, 2, 3, 4]

        # Randomly choose sizes for each symbol to add visual variety
        s = random.choices(available_sizes, k=len(self.symbol_images))
        s = sorted(s, reverse=True)  # Sort by size (largest first) for better packing

        # Use circlify to calculate optimal circle positions within the card
        circles = circlify.circlify(s)

        cx, cy = self.card_diameter_px // 2, self.card_diameter_px // 2

        ids = list(dict.fromkeys(self.symbol_images))
        random.shuffle(ids)

        margin = 5  # Margin from card edge in pixels
        diameter = self.card_diameter_px

        # Place each symbol on the card
        for i, circle in zip(self.symbol_images.keys(), circles):
            # Convert normalized circle coordinates to pixel coordinates
            cx = margin + (circle.x + 1) / 2 * (diameter - 2 * margin)
            cy = margin + (circle.y + 1) / 2 * (diameter - 2 * margin)

            # Calculate radius with 10% reduction to leave space between circles
            r = circle.r * (diameter - 2 * margin) / 2 * 0.9

            # Random rotation angle for visual interest
            angle = random.random() + random.randint(0, 359)

            # Place and draw the symbol on the card
            image = self.symbol_images[i]
            image.place(int(cx), int(cy), int(r), angle)
            self.draw_symbol(image)
            self.placed.append(image)

        if len(self.placed) < len(self.symbol_images):
            raise RuntimeError(
                "Could not place all the symbols in the card. "
                "Please consider increasing the number of retries. "
                f"{self}"
            )

    def draw_symbol(self, s: Symbol) -> None:
        """Composite a symbol image onto the card at its calculated position.

        Args:
            s: The Symbol object to draw on the card.
        """
        self.image.alpha_composite(
            s.image, (s.x - s.image.width // 2, s.y - s.image.height // 2)
        )

    def save(self):
        """Save the card image to a PNG file."""
        self.image.save(self.filename, "PNG")

    def no_overlap(self, symbol: Symbol) -> bool:
        """Check that a symbol does not overlap with already placed symbols.

        Args:
            symbol: The Symbol object to check for overlaps.

        Returns:
            True if the symbol does not overlap with any placed symbol, False otherwise.
        """
        for s in self.placed:
            # Calculate distance between symbol centers
            dist = math.hypot(s.x - symbol.x, s.y - symbol.y)
            # Add 5% buffer to ensure proper spacing
            if dist < (symbol.radius + s.radius) * 1.05:
                return False
        return True

    def __str__(self) -> str:
        """Return a string representation of the Card.

        Returns:
            A string containing the card filename and placed symbols.
        """
        return f"Card({self.filename},{[s.__str__() for s in self.placed]})"
