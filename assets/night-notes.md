# Night profile assets

`night-animals.gif` is a 960 × 280, 24-second loop with a fox, rabbit, cat, twinkling stars, and three meteor passes. `night-animals-still.png` is the still alternative. Animal sheets were made with the built-in image generation tool.

Rebuild with `python scripts/render-night-banner.py`. Requires Pillow and DejaVu fonts; `FONT_DIR` can override the font location. The existing woodland and terminal assets remain available but are not embedded in the profile.

Toolkit rows use locally stored [Devicon](https://github.com/devicons/devicon) SVGs under the included [MIT license](./icons/LICENSE). Run `python scripts/render-toolkit.py` to rebuild the labeled rows. Product marks belong to their respective owners.

The streak card uses [GitHub Readme Streak Stats](https://github.com/DenverCoder1/github-readme-streak-stats). The footer uses [GitHub Readme Quotes](https://github.com/PiyushSuthar/github-readme-quotes). Both are external services. GitHub image caching affects refresh timing, so the quote is not guaranteed to change on every page reload.

## Rabbit prompt

```text
Use case: stylized-concept. Create a transparent walk-cycle sprite sheet for a cozy nighttime developer profile. EXACTLY four columns and two rows, eight equal-sized cells, one animal per cell. All poses full-body side profile facing RIGHT, same scale, body proportions and baseline. Eight successive phases of a natural walking gait with alternating planted and lifted paws. Warm hand-painted storybook illustration, subtle dimensional shading, soft fur. Generous transparent margins in each cell, no grid lines, numbers, text, scenery, ground or shadows. True alpha transparency. Subject: a small fluffy cream rabbit with long ears, a round little tail, warm beige shading and dark brown eyes. Eight successive gentle stepping/hopping poses.
```

## Cat prompt

```text
Use case: stylized-concept. Asset: transparent walk-cycle sprite sheet. EXACTLY four columns and two rows, eight equal-sized square cells, one animal per cell. Subject: one consistent cute fluffy silver-gray tabby kitten with cream muzzle and chest, green eyes, long gently curved tail. All eight full-body side-profile poses face RIGHT, same scale and floor baseline, ample clear margins. Eight sequential walking poses: contact, down, passing, up, opposite contact, down, passing, up. Show clearly different leg positions and alternating paws; consistent torso, subtle tail movement. Warm hand-painted storybook illustration with soft fur and dimensional shading for a cozy night-sky banner. No text, numbers, grid, background, floor, or cast shadow. True transparent background.
```

The original fox prompt is in [woodland-notes.md](./woodland-notes.md).
