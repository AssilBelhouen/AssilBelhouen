# Behind the terminal

This profile borrows its palette, terminal language, and engineering focus from [my portfolio](https://assil-belhouene-portfolio.vercel.app/).

The portrait is actual ASCII: a head-and-shoulders crop of my photograph, a manually defined silhouette, and luminance-to-character mapping. A compact 44-column sketch uses one pale text color, so the characters read as typography instead of a shaded photograph. Each character has a fixed cell position in the SVG. The plain-text version contains the same characters. No generated illustration or embedded photograph is used.

The wide hero pairs the sketch with a neofetch-style engineering summary. The layout is inspired by [Andrew6rant's profile](https://github.com/Andrew6rant/Andrew6rant); the artwork, generator, and profile copy here are original. No third-party portrait, code, or statistics are copied.

The card uses near-black `#0D1410`, green `#00FF88`, pale text `#DCE6DF`, and muted text `#859189`, keeping the terminal aesthetic of my portfolio. A stacked mobile layout is provided through a responsive `<picture>` source; clients that ignore that source receive the wide hero. The surrounding README follows the reader's GitHub theme. The SVGs have no JavaScript, remote fonts, embedded raster images, or external dependencies.

## Reproduce locally

Use Python 3.12 and install the pinned dependency in a virtual environment:

```sh
python -m pip install -r tools/requirements.txt
python tools/generate_art.py --photo /path/to/assil_belhouene.png
```

The original 1254 × 1254 photograph stays outside the repository. The silhouette and crop are tailored to that photo; other photographs need adjusted coordinates. Optional `--preview-dir /path/to/previews` writes comparison PNGs using Windows Consolas. Preview files are not published.

Public career, project, education, and credential descriptions were checked against the portfolio on October 11, 2026. Contact links use the public portfolio email and LinkedIn. No private project details, phone number, or reconstructed commit dates are included.
