# Behind the terminal

This profile borrows its palette, terminal language, and engineering focus from [my portfolio](https://assil-belhouene-portfolio.vercel.app/).

The portrait is actual ASCII: a head-and-shoulders crop of my photograph, a manually defined silhouette, softened grayscale contrast, light smoothing, and luminance-to-character mapping. Dot-like punctuation replaces heavy symbols and horizontal strokes; natural light values keep the face brighter than the hair. Muted sage and mint tones, occasional empty cells, and generous margins make the portrait less intense. Each character has a fixed cell position in the SVG. The plain-text version contains the same characters. No generated illustration or embedded photograph is used.

The wide hero uses `#070A08`, `#00FF88`, `#F5FFF8`, and `#859189`. A compact portrait layout is provided through a responsive `<picture>` source; clients that ignore that source receive the wide hero. The surrounding README follows the reader's GitHub theme. The SVGs have no JavaScript, remote fonts, embedded raster images, or external dependencies.

## Reproduce locally

Use Python 3.12 and install the pinned dependency in a virtual environment:

```sh
python -m pip install -r tools/requirements.txt
python tools/generate_art.py --photo /path/to/assil_belhouene.png
```

The original 1254 × 1254 photograph stays outside the repository. The silhouette and crop are tailored to that photo; other photographs need adjusted coordinates. Optional `--preview-dir /path/to/previews` writes comparison PNGs using Windows Consolas. Preview files are not published.

Public career, project, education, and credential descriptions were checked against the portfolio on October 11, 2026. Contact links use the public portfolio email and LinkedIn. No private project details, phone number, or reconstructed commit dates are included.
