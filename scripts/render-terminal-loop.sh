#!/usr/bin/env bash
# Encode a gentle four-second float from the original transparent artwork.
# Requires FFmpeg with libavfilter. Run from any directory.
set -euo pipefail
cd "$(dirname "$0")/.."
ffmpeg -hide_banner -loglevel error -y \
  -f lavfi -i 'color=c=0x0d1117:s=320x320:r=20:d=4' \
  -loop 1 -framerate 20 -i assets/terminal-3d.png \
  -filter_complex "[1:v]scale=280:280:flags=lanczos,format=rgba[obj];[0:v][obj]overlay=x=20:y='20+6*sin(2*PI*t/4)':shortest=1,split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a" \
  -t 4 -loop 0 assets/terminal-float.gif
