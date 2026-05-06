# Codex Pets Wapuu

Wapuu for Codex Pets.

This repository packages Wapuu as a Codex-compatible pet. It keeps Wapuu as
Wapuu: the artwork is based on the original Wapuu source, and animation work is
intended to stay within small, respectful changes to hands, legs, tail, posture,
and expression.

## Respect For Wapuu

Wapuu is copyright カネウチカズコさん (Kazuko Kaneuchi).

This project is made with deep respect for カネウチカズコさん's original character
design and for the WordPress community that has cared for Wapuu over the years.
The goal is not to redesign Wapuu or replace it with a generated lookalike. The
goal is to let the original Wapuu sit inside Codex Pets while preserving the
character's identity and charm.

The original Wapuu artwork is distributed under the GNU General Public License.
Please preserve the copyright and GPL license notices when copying, modifying,
packaging, or redistributing Wapuu-derived assets.

This repository includes the GPL text at the repository root:

- `LICENSE.txt`
- `LICENSE-ja.txt`
- `NOTICE.txt`
- `THIRD_PARTY_NOTICES.md`

## Current Package

The generated Codex pet package is in:

```text
pets/wapuu/
  pet.json
  spritesheet.webp
  spritesheet.png
  contact-sheet.png
  validation.json
  NOTICE.txt
  LICENSE.txt
  LICENSE-ja.txt
```

`spritesheet.webp` is the file referenced by `pet.json`. `contact-sheet.png` is
included for visual review.

## Build

The build script uses the upstream Wapuu image from `third_party/wapuu`.
`third_party/` is ignored by Git because it is a local copy of the upstream
repository.

If the source artwork is missing, fetch it first:

```powershell
git clone https://github.com/jawordpressorg/wapuu.git .\third_party\wapuu
git -C .\third_party\wapuu checkout b5836525649270dd942012dfe526c435be97618b
```

Recorded upstream source commit:

```text
b5836525649270dd942012dfe526c435be97618b
```

Then rebuild the pet:

```powershell
python .\scripts\build_wapuu_pet.py
```

Validate the atlas:

```powershell
python .\.codex\skills\hatch-pet\scripts\validate_atlas.py .\pets\wapuu\spritesheet.png --json-out .\pets\wapuu\validation.json
```

## Pet Format

This repository follows the installed hatch-pet skill as the Codex pet contract:

```text
.codex/skills/hatch-pet/SKILL.md
```

The atlas is `1536x1872`, arranged as 8 columns by 9 rows of `192x208` cells.
Unused cells must remain transparent.

## Contributions Wanted

The current animation is intentionally conservative. Help is welcome, especially
for:

- reducing jagged edges while keeping the original Wapuu identity
- improving the loading animation so Wapuu's left hand taps the W ball more
  naturally
- creating cleaner hand, leg, tail, or expression frame edits from the original
  source artwork

Please do not submit a generated replacement character. Wapuu should remain
recognizably Wapuu.

## License

Wapuu is copyright カネウチカズコさん (Kazuko Kaneuchi).

The original Wapuu artwork used here is GPL licensed. See:

- `LICENSE.txt`
- `LICENSE-ja.txt`
- `NOTICE.txt`
- `THIRD_PARTY_NOTICES.md`
- `pets/wapuu/LICENSE.txt`
- `pets/wapuu/LICENSE-ja.txt`
- `pets/wapuu/NOTICE.txt`

The bundled hatch-pet skill under `.codex/skills/hatch-pet/` includes its own
Apache License 2.0 text at `.codex/skills/hatch-pet/LICENSE.txt`.

The upstream source repository is:

```text
https://github.com/jawordpressorg/wapuu
```

Recorded upstream source commit:

```text
b5836525649270dd942012dfe526c435be97618b
```
