# 15 Puzzle

A simple Python implementation of the classic 15-puzzle game.

This project includes:
- a graphical board built with Tkinter
- keyboard controls for moving tiles
- a shuffled board reset option
- optional solver helpers in the `solver/` folder

## Requirements

- Python 3.10+ recommended
- `Pillow`
- `numpy`
- Tkinter (usually included with Python on Windows and macOS)

## Setup

From the project folder, create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the game

```powershell
python main.py
```

## Controls

Use the arrow keys to move the empty space around the board:
- Up
- Down
- Left
- Right

You can also use:
- `W`, `A`, `S`, `D` keys
- `L` to make a random solver move
- `R` to reset / shuffle the board

## Notes

This is a lightweight puzzle app intended for local play and experimentation. If Tkinter is missing on your system, install the Python Tk package for your OS before running it.

## AI

Some segments in thie project were generatoed by AI, are are labeled as such.
For example, this README was made with Copilot Free agent
