from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Iterable

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "third_party" / "wapuu" / "wapuu-original" / "wapuu-original.png"
OUT_DIR = ROOT / "pets" / "wapuu"
WAPUU_SOURCE_REPO = "https://github.com/jawordpressorg/wapuu"
WAPUU_SOURCE_COMMIT = "b5836525649270dd942012dfe526c435be97618b"
CELL_W = 192
CELL_H = 208
COLS = 8
ROWS = 9

RESAMPLE = Image.Resampling.LANCZOS


def alpha_trim(image: Image.Image) -> Image.Image:
    bbox = image.getbbox()
    if bbox is None:
        raise ValueError(f"source has no visible pixels: {SOURCE}")
    return image.crop(bbox)


def fit_sprite(source: Image.Image, max_w: int = 168, max_h: int = 188) -> Image.Image:
    sprite = alpha_trim(source.convert("RGBA"))
    scale = min(max_w / sprite.width, max_h / sprite.height)
    size = (round(sprite.width * scale), round(sprite.height * scale))
    return sprite.resize(size, RESAMPLE)


def transformed(sprite: Image.Image, *, scale: float = 1.0, angle: float = 0.0, flip: bool = False) -> Image.Image:
    frame = sprite
    if flip:
        frame = frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if scale != 1.0:
        size = (round(frame.width * scale), round(frame.height * scale))
        frame = frame.resize(size, RESAMPLE)
    if angle:
        frame = frame.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    return frame


def cell(sprite: Image.Image, *, x: int = 0, y: int = 0, scale: float = 1.0, angle: float = 0.0, flip: bool = False) -> Image.Image:
    frame = transformed(sprite, scale=scale, angle=angle, flip=flip)
    canvas = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
    left = (CELL_W - frame.width) // 2 + x
    top = CELL_H - frame.height - 8 + y
    canvas.alpha_composite(frame, (left, top))
    return canvas


def fill_row(atlas: Image.Image, row: int, frames: Iterable[Image.Image]) -> None:
    for col, frame in enumerate(frames):
        atlas.alpha_composite(frame, (col * CELL_W, row * CELL_H))


def make_contact_sheet(atlas: Image.Image) -> Image.Image:
    border = 1
    sheet = Image.new("RGBA", (COLS * (CELL_W + border) + border, ROWS * (CELL_H + border) + border), (40, 40, 40, 255))
    for row in range(ROWS):
        for col in range(COLS):
            tile = atlas.crop((col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H))
            x = border + col * (CELL_W + border)
            y = border + row * (CELL_H + border)
            checker = Image.new("RGBA", (CELL_W, CELL_H), (238, 238, 238, 255))
            for yy in range(0, CELL_H, 16):
                for xx in range(0, CELL_W, 16):
                    if (xx // 16 + yy // 16) % 2:
                        checker.paste((214, 214, 214, 255), (xx, yy, xx + 16, yy + 16))
            checker.alpha_composite(tile)
            sheet.alpha_composite(checker, (x, y))
    return sheet


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sprite = fit_sprite(Image.open(SOURCE))
    atlas = Image.new("RGBA", (COLS * CELL_W, ROWS * CELL_H), (0, 0, 0, 0))

    # 0 idle: subtle breathing.
    fill_row(
        atlas,
        0,
        [
            cell(sprite, y=0, scale=1.00),
            cell(sprite, y=-1, scale=1.01),
            cell(sprite, y=-2, scale=1.01),
            cell(sprite, y=-1, scale=1.00),
            cell(sprite, y=0, scale=0.995),
            cell(sprite, y=0, scale=1.00),
        ],
    )

    # 1 running-right: directional bob without mirroring the W mark.
    fill_row(
        atlas,
        1,
        [
            cell(sprite, x=-8, y=0, angle=-4),
            cell(sprite, x=-5, y=-4, angle=-2),
            cell(sprite, x=-1, y=-2, angle=1),
            cell(sprite, x=3, y=0, angle=3),
            cell(sprite, x=8, y=-3, angle=4),
            cell(sprite, x=5, y=-1, angle=2),
            cell(sprite, x=1, y=1, angle=-1),
            cell(sprite, x=-4, y=0, angle=-3),
        ],
    )

    # 2 running-left: reverse the travel offsets, still keep the source art unmirrored.
    fill_row(
        atlas,
        2,
        [
            cell(sprite, x=8, y=0, angle=4),
            cell(sprite, x=5, y=-4, angle=2),
            cell(sprite, x=1, y=-2, angle=-1),
            cell(sprite, x=-3, y=0, angle=-3),
            cell(sprite, x=-8, y=-3, angle=-4),
            cell(sprite, x=-5, y=-1, angle=-2),
            cell(sprite, x=-1, y=1, angle=1),
            cell(sprite, x=4, y=0, angle=3),
        ],
    )

    # 3 waving: small friendly whole-body lift, preserving the original silhouette.
    fill_row(
        atlas,
        3,
        [
            cell(sprite, y=0, angle=0),
            cell(sprite, y=-4, angle=-5),
            cell(sprite, y=-7, angle=-8),
            cell(sprite, y=-2, angle=-3),
        ],
    )

    # 4 jumping: anticipation, lift, peak, return.
    fill_row(
        atlas,
        4,
        [
            cell(sprite, y=4, scale=0.99),
            cell(sprite, y=-8, scale=1.00),
            cell(sprite, y=-20, scale=1.00, angle=-2),
            cell(sprite, y=-8, scale=1.00),
            cell(sprite, y=0, scale=1.00),
        ],
    )

    # 5 failed: droop and settle. No extra marks or detached effects.
    fill_row(
        atlas,
        5,
        [
            cell(sprite, y=0),
            cell(sprite, y=3, angle=3),
            cell(sprite, y=7, angle=6),
            cell(sprite, y=10, angle=9, scale=0.985),
            cell(sprite, y=8, angle=7, scale=0.985),
            cell(sprite, y=10, angle=9, scale=0.98),
            cell(sprite, y=8, angle=7, scale=0.985),
            cell(sprite, y=6, angle=5, scale=0.99),
        ],
    )

    # 6 waiting: patient small rocking loop.
    fill_row(
        atlas,
        6,
        [
            cell(sprite, y=0),
            cell(sprite, x=-2, y=-2, angle=-2),
            cell(sprite, x=-3, y=-1, angle=-3),
            cell(sprite, x=0, y=0),
            cell(sprite, x=2, y=-2, angle=2),
            cell(sprite, x=3, y=-1, angle=3),
        ],
    )

    # 7 running/loading: conservative active loop without local hand redrawing.
    fill_row(
        atlas,
        7,
        [
            cell(sprite, y=0, angle=0),
            cell(sprite, y=-2, angle=-4),
            cell(sprite, y=-5, angle=-8),
            cell(sprite, y=-2, angle=-4),
            cell(sprite, y=1, angle=2),
            cell(sprite, y=-1, angle=-2),
        ],
    )

    # 8 review: focused inspecting/thinking motion.
    fill_row(
        atlas,
        8,
        [
            cell(sprite, y=0, scale=1.00),
            cell(sprite, x=-1, y=-1, angle=-1),
            cell(sprite, x=-2, y=-2, angle=-2),
            cell(sprite, x=-1, y=-1, angle=-1),
            cell(sprite, x=1, y=0, angle=1),
            cell(sprite, x=0, y=0, angle=0),
        ],
    )

    atlas_path = OUT_DIR / "spritesheet.png"
    webp_path = OUT_DIR / "spritesheet.webp"
    contact_path = OUT_DIR / "contact-sheet.png"
    atlas.save(atlas_path)
    atlas.save(webp_path, lossless=True, quality=100, method=6)
    make_contact_sheet(atlas).save(contact_path)

    manifest = {
        "id": "wapuu",
        "displayName": "Wapuu",
        "description": "The original GPL Wapuu mascot as a Codex pet.",
        "spritesheetPath": "spritesheet.webp",
    }
    (OUT_DIR / "pet.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    notice = (
        "This pet reuses the Wapuu source art from jawordpressorg/wapuu under GPL-2.0.\n"
        f"Source: {WAPUU_SOURCE_REPO}\n"
        f"Source commit: {WAPUU_SOURCE_COMMIT}\n"
        "See third_party/wapuu/LICENSE.txt and third_party/wapuu/LICENSE-ja.txt.\n"
    )
    (OUT_DIR / "NOTICE.txt").write_text(notice, encoding="utf-8")
    shutil.copyfile(ROOT / "third_party" / "wapuu" / "LICENSE.txt", OUT_DIR / "LICENSE.txt")
    shutil.copyfile(ROOT / "third_party" / "wapuu" / "LICENSE-ja.txt", OUT_DIR / "LICENSE-ja.txt")

    print(f"wrote {atlas_path}")
    print(f"wrote {webp_path}")
    print(f"wrote {OUT_DIR / 'pet.json'}")
    print(f"wrote {contact_path}")


if __name__ == "__main__":
    main()
