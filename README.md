# tmdb-movie-rename
Simple script renaming movie files optimized for Kodi library scan.

## Features:
- Query TMDB for movies based on search term and display short overview
- Rename file to "moviename (year)"
- Append Kodi 3D Flag to filename (".3d.mvc", etc.)
- Move file to one of the specified library directories

## Preperation:
Install the dependencies via pip:
- tmdbsimple
- configparser
- argparse

Copy configuration example to `~/.config/tmdb-movie-rename/config.ini`, add TMDB api key and edit directories if needed.

## Usage:
`python tmdb-movie-rename.py [movie-folder]`
