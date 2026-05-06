# Repository Guidelines

## Purpose

This repository builds Codex-compatible Wapuu pet assets.

The Wapuu character must remain recognizably Wapuu. Do not use generative AI to
replace Wapuu with a substantially different character, species, mascot, or style.
Animation work should modify only the minimum needed parts of the original design,
such as hands, legs, tail, posture, and facial expression.

## Copyright And License

Wapuu is copyright Kazuko Kaneuchi.

The original Wapuu source artwork used by this repository is distributed under
the GNU General Public License. Preserve the original copyright and GPL license
notices when copying, modifying, packaging, or redistributing Wapuu-derived pet
assets.

Keep license files with generated pet packages when they contain Wapuu-derived
art. For the current package, `pets/wapuu/NOTICE.txt`, `pets/wapuu/LICENSE.txt`,
and `pets/wapuu/LICENSE-ja.txt` must stay with `pet.json` and `spritesheet.webp`.

## Source Artwork

The upstream Wapuu source repository is:

```text
https://github.com/jawordpressorg/wapuu
```

`third_party/` is ignored by Git and may contain a local clone of that upstream
repository. Do not treat `third_party/` as original project source.

## Pet Creation Workflow

Use the installed hatch-pet skill as the contract reference for Codex pet format,
sprite atlas dimensions, row names, frame counts, validation, and package shape:

```text
.codex/skills/hatch-pet/SKILL.md
```

For deterministic Wapuu builds, prefer repository scripts such as:

```powershell
python .\scripts\build_wapuu_pet.py
```

Generated packages should be written under `pets/<pet-id>/`.

## Wapuu Editing Rules

When creating or revising Wapuu pet frames:

- Keep the original Wapuu identity, proportions, colors, W ball, tail, ears, and
  overall silhouette unless a specific animation requires a small local change.
- Prefer direct edits to the original PNG/SVG source, or deterministic transforms,
  over prompt-only image generation.
- If generative tools are used, use the original Wapuu art as a strict reference
  and accept only outputs that preserve Wapuu's identity.
- Limit changes to animation-relevant parts: hand position, leg position, tail
  curve, posture, body tilt, eye shape, mouth shape, and small expression changes.
- Do not add unrelated props, scenery, text, logos beyond the existing W ball,
  decorative effects, shadows, or detached particles.
- Do not simplify Wapuu into a generic yellow animal or redesign it into a new
  pet.

## Validation

Before considering a pet package complete, validate the atlas:

```powershell
python .\.codex\skills\hatch-pet\scripts\validate_atlas.py .\pets\wapuu\spritesheet.png --json-out .\pets\wapuu\validation.json
```

The atlas must be `1536x1872`, use `192x208` cells, preserve transparent unused
cells, and keep `pet.json` next to `spritesheet.webp`.
