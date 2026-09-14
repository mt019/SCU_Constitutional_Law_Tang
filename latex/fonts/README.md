# Traditional Chinese Font Pack

This folder is the reusable Traditional Chinese font pack for quote cards and other LaTeX / design work.

## Layout

The font files themselves live outside this repository, in `~/Documents/NTU/1142/font-lab/packs/scu-constitutional/`. Set `SCU_FONT_PACK` to point the scripts at another location.

- `fonts/` (in the pack): usable font files copied from the generated comparison workspace.
- `categories/` (in the pack): curated browsing groups. Symlinks point back to `fonts/`; newly imported experimental fonts live in the category folder where they are first being tested.
- `compare/` (in the pack): the current comparison PDF/PNG/TeX snapshot.
- `scripts/install_user_fonts.sh`: install the pack into the current macOS user's font path.
- `scripts/uninstall_user_fonts.sh`: remove installed files with the `SCUQuoteCards-` prefix.
- `scripts/list_font_names.sh`: inspect registered font names after installation.
- `manifest.tsv`: source, license, and usage notes.
- `category_manifest.tsv`: category-level purpose and recommended use.

## Install

Run from this repository root:

```sh
latex/fonts/scripts/install_user_fonts.sh
```

The script installs fonts directly into `~/Library/Fonts` with `SCUQuoteCards-` filename prefixes, the same prefix `uninstall_user_fonts.sh` removes. Override it with `FONT_INSTALL_PREFIX`.

To remove only this managed pack:

```sh
latex/fonts/scripts/uninstall_user_fonts.sh
```

## Categories

- `elegant-intellectual`: stable Ming/Sung faces for class notes, legal quotes, serious cards, and readable paragraph text.
- `handwriting-accent`: handwritten faces for titles, signatures, and short accent lines.
- `typewriter-ink`: typewriter, woodblock, old movable-type, heavy ink, and nostalgic print faces. The imported `2904-复古怀旧字体` pack is staged here for visual testing.

## Current Picks

- Main old-book card: `HuiwenMincho-Improved.ttf`
- Elegant serif candidates: `ChironSungHK-Text-R.ttf`, `GenWanMin2-R.ttc`, `GenRyuMin2-R.ttc`, `GenYoMin2-R.ttc`
- Handwritten accent: `ChenYuluoyan-2.0-Thin.ttf`
- Friendly handwritten serif: `Iansui-Regular.ttf`
- Woodblock / ink accent: `qiji-combo.ttf`, `xiangcui-typewriter-w35.ttf`, `xiangcui-typewriter-w40.ttf`

`NoroshiCode` was deliberately excluded from this pack because it looked too technical for the quote-card style.

The `2904-复古怀旧字体` imports are kept as local visual candidates. Several files came from a downloaded bundle with mixed or unclear license notes, so confirm licensing before public or commercial use.
