# Night observatory profile

The imagegen concept in `night-observatory-concept.png` guided the composition, palette, landscape, and hierarchy. It is a reference, not a screenshot of the final README. Its illustrative labels and badges are not factual profile content.

The implementation uses a separately generated landscape, real text, vendored technology logos, existing credentials, and live streak and quote widgets. It replaces repeated gradient cards with compact ruled sections. GitHub still controls the page background and spacing between embedded images.

## Rebuild

Run from the repository root:

```sh
python scripts/render-observatory.py
python scripts/render-observatory-panels.py
python scripts/render-toolkit.py
```

The animation renderer requires Pillow and DejaVu fonts. `FONT_DIR` can override the font directory. The SVG generators use Python's standard library. The animation has 240 frames at 10 fps and loops every 24 seconds. The desktop GIF is approximately 2.1 MB; the separate 420px mobile GIF is approximately 1.1 MB. Mobile picture sources activate below 600px.

The production landscape and full-page concept were generated with the built-in image generation tool. Exact prompts are saved in `concept-prompt.md` and `landscape-prompt.md`. Original animal prompts remain in `assets/woodland-notes.md` and `assets/night-notes.md`. The footer is a composed crop of the same landscape, with a separate mobile composition.

## Review and validation

Fresh agents independently reviewed the design and implemented the toolkit and body panels. Review caught the desktop hero's small text on phones; the final design has a separately rendered mobile animation. XML, local source references, both GIF durations/frame counts, and GitHub Markdown rendering were verified. Desktop and 390px browser checks found all images loaded and no horizontal overflow. Browser text bounds for the mobile SVGs showed no clipping.

Live statistics and quotes depend on external services and GitHub image caching. The mockup's statistics and quote are not used as profile data. Original earlier assets remain in the repository but are no longer embedded in the README.
