from __future__ import annotations

from PIL import Image, ImageDraw
from PIL.Image import Resampling


class Symbol:
    """Represents a symbol image that can be placed on Dobble cards.

    Handles image loading, cropping to circular shape, resizing, and rotation
    for placement on cards.
    """

    x: int = 0  # X coordinate of symbol center on card
    y: int = 0  # Y coordinate of symbol center on card
    radius: int = 0  # Radius of the symbol in pixels
    angle: float = 0.0  # Rotation angle in degrees

    def __init__(self, image_path: str, read: bool = True):
        """Initialize a Symbol from an image file.

        Args:
            image_path: Path to the image file.
            read: If True, immediately load the image. If False, defer loading.
        """
        self.image_path = image_path
        if read:
            self.image = Image.open(image_path).convert("RGBA")

    def crop_circle(self) -> None:
        """Crop the image to a circular mask with transparent background."""
        mask = Image.new("L", self.image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, self.image.size[0], self.image.size[1]), fill=255)
        self.image.putalpha(mask)

    def place(
        self,
        x: int,
        y: int,
        r: int,
        angle: float,
        resampling=Resampling.LANCZOS,
    ) -> None:
        """Place the symbol at a specific position, size, and rotation on a card.

        Args:
            x: X coordinate of the symbol center in pixels.
            y: Y coordinate of the symbol center in pixels.
            r: Radius (size) of the symbol in pixels.
            angle: Rotation angle in degrees.
            resampling: Resampling filter for image resizing (default: LANCZOS).
        """
        self.x = x
        self.y = y
        self.radius = r
        self.angle = angle
        self._gen()

    def _gen(self) -> None:
        """Resize and rotate the image based on placement parameters.

        This internal method generates the final image representation
        by applying the radius (size) and angle (rotation).
        """
        self.image = self.image.resize(
            (self.radius * 2, self.radius * 2), resample=Resampling.LANCZOS
        ).rotate(self.angle, expand=False)

    def copy(self):
        """Create a deep copy of this Symbol.

        Returns:
            A new Symbol instance with a copied image but same image path.
        """
        clone = Symbol(
            self.image_path,
            read=False,
        )
        clone.image = self.image.copy()
        return clone

    def __repr__(self) -> str:
        """Return a string representation of the Symbol.

        Returns:
            A string containing the image path and position coordinates.
        """
        return f"Symbol({self.image_path},{self.x},{self.y})"
