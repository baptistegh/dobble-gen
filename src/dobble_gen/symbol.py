from __future__ import annotations

from PIL import Image, ImageDraw
from PIL.Image import Resampling


class Symbol:
    x: int = 0
    y: int = 0
    radius: int = 0
    angle: float = 0.0

    def __init__(self, image_path: str, read: bool = True):
        self.image_path = image_path
        if read:
            self.image = Image.open(image_path).convert("RGBA")

    def crop_circle(self) -> None:
        """Crop the image into a circle."""
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
        self.x = x
        self.y = y
        self.radius = r
        self.angle = angle
        self._gen()

    def _gen(self):
        self.image = self.image.resize(
            (self.radius * 2, self.radius * 2), resample=Resampling.LANCZOS
        ).rotate(self.angle, expand=False)

    def copy(self):
        """Copy the image."""
        clone = Symbol(
            self.image_path,
            read=False,
        )
        clone.image = self.image.copy()
        return clone

    def __repr__(self) -> str:
        return f"Symbol({self.image_path},{self.x},{self.y})"
