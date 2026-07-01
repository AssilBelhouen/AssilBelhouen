# Behind the terminal

This profile borrows its palette, terminal language, and engineering focus from [my portfolio](https://assil-belhouene-portfolio.vercel.app/).

The portrait is actual ASCII, converted from an AI-assisted monochrome sketch based on my second photograph (white polo and glasses). OpenAI's built-in image generation tool simplified the background and facial contours; the final README portrait is a deterministic 52-column conversion of that sketch, not embedded raster artwork. The sketch is an artistic likeness, not an unaltered photograph.

Each character has a fixed cell position and one pale text color in the SVG. The plain-text version contains the same characters. The [generated source sketch](assets/portrait-source.png) and [generation prompt](assets/portrait-prompt.txt) are included for transparency and reproducible ASCII conversion. Original photographs remain outside this repository.

The wide hero pairs the sketch with a neofetch-style engineering summary. The layout is inspired by [Andrew6rant's profile](https://github.com/Andrew6rant/Andrew6rant); the artwork, generator, and profile copy here are original. No third-party portrait, code, or statistics are copied.

The card uses near-black `#0D1410`, green `#00FF88`, pale text `#DCE6DF`, and muted text `#859189`, keeping the terminal aesthetic of my portfolio. A stacked mobile layout is provided through a responsive `<picture>` source; clients that ignore that source receive the wide hero. The surrounding README follows the reader's GitHub theme. The SVGs have no JavaScript, remote fonts, embedded raster images, or external dependencies.

## Reproduce locally

Use Python 3.12 and install the pinned dependency in a virtual environment:

```sh
python -m pip install -r tools/requirements.txt
python tools/generate_art.py
```

The generator uses the included sketch by default. Optional `--photo /path/to/another-sketch.png` accepts a white-background sketch with matching composition. Other inputs may need adjusted crop coordinates. Optional `--preview-dir /path/to/previews` writes comparison PNGs using Windows Consolas. Preview files are not published. The included source preserves the selected imagegen result; regenerating with the same prompt may produce a different sketch.

Public career, project, education, and credential descriptions were checked against the portfolio on October 11, 2026. Contact links use the public portfolio email and LinkedIn. No private project details, phone number, or reconstructed commit dates are included.
