from PIL import Image, ImageDraw
import math
import random

from dobble_gen.symbol import Symbol

import circlify


class Card:
    placed: list[Symbol]

    def __init__(
        self,
        card_diameter_px: int,
        symbol_images: dict[int, Symbol],
        filename: str,
    ):
        self.card_diameter_px = card_diameter_px
        self.symbol_images = symbol_images
        self.filename = filename
        self.placed = []
        self.image = Image.new(
            "RGBA", (card_diameter_px, card_diameter_px), (255, 255, 255, 0)
        )
        self.draw = ImageDraw.Draw(self.image)
        self.border_color = (50, 50, 50, 255)
        self.border_width = max(2, self.card_diameter_px // 200)
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
        """Try to draw circular Dobble card with all constraints."""
        available_sizes = [1, 2, 3, 4]

        # randomly choose sizes of images
        s = random.choices(available_sizes, k=len(self.symbol_images))
        s = sorted(s, reverse=True)

        # create circles packed in circle
        circles = circlify.circlify(s)

        cx, cy = self.card_diameter_px // 2, self.card_diameter_px // 2

        ids = list(dict.fromkeys(self.symbol_images))
        random.shuffle(ids)

        margin = 5
        diameter = self.card_diameter_px

        for i, circle in zip(self.symbol_images.keys(), circles):
            # calculate the center and diameter of a circle
            cx = margin + (circle.x + 1) / 2 * (diameter - 2 * margin)
            cy = margin + (circle.y + 1) / 2 * (diameter - 2 * margin)

            r = (
                circle.r * (diameter - 2 * margin) / 2 * 0.9
            )  # leave some space between circles

            angle = random.random() + random.randint(0, 359)

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
        self.image.alpha_composite(
            s.image, (s.x - s.image.width // 2, s.y - s.image.height // 2)
        )

    def save(self):
        """Save the card to a file."""
        self.image.save(self.filename, "PNG")

    def no_overlap(self, symbol: Symbol):
        """Check that an image (center x, y, radius r) does not overlap the others."""
        for s in self.placed:
            dist = math.hypot(s.x - symbol.x, s.y - symbol.y)
            if dist < (symbol.radius + s.radius) * 1.05:
                return False
        return True

    def __str__(self):
        return f"Card({self.filename},{[s.__str__() for s in self.placed]})"
