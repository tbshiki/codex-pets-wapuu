# Wapuu Pet

This repository builds a Codex-compatible Wapuu pet from the original Wapuu artwork.
Wapuu is copyright Kazuko Kaneuchi and is distributed under the GNU General Public
License.

The source artwork is kept in `third_party/wapuu`, cloned from:

```text
https://github.com/jawordpressorg/wapuu
```

`third_party/` is intentionally ignored by Git because it is a local copy of the
upstream repository. If it is missing, fetch it with:

```powershell
git clone https://github.com/jawordpressorg/wapuu.git .\third_party\wapuu
```

The generated pet package is written to:

```text
pets/wapuu/
  pet.json
  spritesheet.webp
  spritesheet.png
  contact-sheet.png
  NOTICE.txt
  LICENSE.txt
  LICENSE-ja.txt
```

Build it with:

```powershell
python .\scripts\build_wapuu_pet.py
```

The current animation keeps the original Wapuu image intact and uses only placement,
scale, and rotation changes per frame. Future frame work should keep Wapuu as Wapuu
and limit edits to animation-relevant parts such as hands, legs, tail, posture, and
expression. The `running` row is treated as a loading loop: Wapuu leans toward the W
ball as if tapping it.

The original Wapuu files are GPL-2.0. See `third_party/wapuu/LICENSE.txt` and
`third_party/wapuu/LICENSE-ja.txt`.
