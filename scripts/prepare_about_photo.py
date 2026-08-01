#!/usr/bin/env python3
"""Build responsive About-page derivatives from the preserved John source photo."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "images" / "about-john" / "john-krause-original.png"
DESTINATION = SOURCE.parent


def resize_to_width(image: Image.Image, width: int) -> Image.Image:
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing preserved source photo: {SOURCE}")
    with Image.open(SOURCE) as source:
        source = source.convert("RGB")
        for width in (640, 960, 1280):
            resize_to_width(source, width).save(
                DESTINATION / f"john-krause-palm-{width}.webp",
                "WEBP",
                quality=82,
                method=6,
            )
        resize_to_width(source, 960).save(
            DESTINATION / "john-krause-palm-960.jpg",
            "JPEG",
            quality=84,
            optimize=True,
            progressive=True,
            subsampling="4:2:0",
        )
    print("Prepared responsive About John photo assets.")


if __name__ == "__main__":
    main()
