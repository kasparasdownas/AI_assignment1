# 2048 AI Project

Implementation of 2048 game with Expectiminimax AI algorithm, GUI, and performance analysis tools.

## Setup

1. Requirements: Python 3.x, pygame, tqdm
2. Install dependencies: `pip install -r requirements.txt`

## Usage

- Play game: `python play.py`
- Run AI analysis: `python headless_stats.py`

### Controls
- Arrow keys: Move tiles
- Space: Turn on AI
- +/-: Adjust AI depth (1-4)
- R: Restart
- ESC: Quit

## Files

- `play.py`: GUI game
- `model.py`: Game logic
- `ai.py`: Expectiminimax algorithm
- `headless_stats.py`: Performance analyzerr

## Notes

- Higher search depths (3+) give better results but run slower
- Results are saved to JSON files
- Fix pygame on macOS: `python -m pip install pygame --user`