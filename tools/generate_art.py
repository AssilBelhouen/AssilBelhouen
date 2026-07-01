"""Regenerate the compact terminal profile from a local photograph.

Usage: python tools/generate_art.py --photo /path/to/assil_belhouene.png
Requires Pillow 12.3.0; the original photograph is never copied.
"""
from neofetch_art import main

if __name__ == '__main__':
    main()
