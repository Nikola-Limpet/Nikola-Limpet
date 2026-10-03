# Woodland animation

The fox sprite sheet was generated with the built-in image generation tool using the user's desktop-panel screenshot as a style reference. `scripts/render-fox-banner.py` assembles the eight poses and moves the fox across a dark olive banner.

- `fox-walk-sheet.png`: original transparent eight-pose artwork.
- `woodland-fox.gif`: 960 × 260 banner, 20-second infinite loop.
- `woodland-fox-still.png`: still alternative.

Run `python scripts/render-fox-banner.py` with Pillow installed to rebuild. The script uses DejaVu fonts; set `FONT_DIR` if they are installed elsewhere.

## Artwork prompt

```text
Use case: stylized-concept
Asset type: eight-frame walking fox animation sprite sheet for a GitHub profile banner.
Reference image: the attached desktop panel establishes cozy storybook animal styling, warm rust-orange fox fur, cream highlights, and a dark olive woodland mood. Do not reproduce the desktop UI.
Primary request: one consistent adorable small orange fox with cream chest and large cream-tipped bushy tail, walking naturally to the RIGHT, strict side profile. Soft hand-painted storybook illustration with subtle dimensional shading and visible fluffy fur, like the tiny fox in the reference.
Layout: EXACTLY 4 columns and 2 rows in a uniform grid of 8 equally sized square cells on a transparent canvas, read left to right top row then bottom row. Each cell contains exactly one full-body fox at the same scale, body center, and floor baseline, ample clear margins. No grid lines. All eight show the SAME fox facing RIGHT. Frame sequence is one seamless complete eight-phase walk cycle: contact, down, passing, up, opposite contact, down, passing, up. Clearly alternating front and rear legs, planted paws on contact frames, lifted paws on passing frames, gentle tail sway. Keep torso and head proportions consistent. Never show fox sitting or sleeping. Never show multiple foxes in one cell. No text, no numbers, no shadows outside the animal, no scenery, no watermark. Genuine transparent background.
```
