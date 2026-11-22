# Chess

A chess game for Windows built with Python, `pygame-ce` and `python-chess`. Play against a Stockfish bot at four difficulty levels, or play a friend on the same computer.

## Features

- **Play vs bot or 2 players:** switch any time with `M`, then choose to continue the current game or restart
- **4 bot difficulties:** Easy, Medium, Hard, Max (Stockfish skill level and thinking time)
- **Full chess rules:** legal moves, check, checkmate, stalemate, draws, castling, en passant (handled by `python-chess`)
- **Pawn promotion:** choose Queen, Rook, Bishop or Knight
- **Legal-move markers:** dots on squares you can move to, red rings on captures
- **Last-move highlight:** see what the bot just played
- **Illegal-move flash:** the target square flashes red
- **Undo:** key or button (in bot mode it takes back both your move and the bot's reply)
- **Material count** for each side
- **4 board themes**
- **Resizable window,** with an in-game help box

## Controls

| Input | Action |
|---|---|
| Click a piece, then a square | Move |
| `U` or the Undo button | Undo |
| `M` | Switch between Bot and 2 Player (then `C` = continue, `R` = restart, `M` = cancel) |
| `T` | Change theme |
| `1` `2` `3` `4` | Bot difficulty (Easy, Medium, Hard, Max) |
| `Q` `R` `B` `N` | Choose a promotion piece |
| `H` or the `?` button | Show / hide help |
| `Esc` | Quit |

## Run it

### Option 1: the exe (Windows)

1. Download `chess__game.exe` from the [Releases](../../releases) page.
2. Double-click it. It takes a few seconds to start.

The exe is **unsigned**, so Windows SmartScreen may say "Windows protected your PC". Click **More info > Run anyway**. The full source is in this repo if you would rather read it or build it yourself.

### Option 2: from source

1. Install Python 3 and the libraries:
   ```
   pip install pygame-ce chess
   ```
2. Download Stockfish from [stockfishchess.org](https://stockfishchess.org/download/), rename the executable to `stockfish.exe`, and put it in the same folder as `chess__game.py`.
3. Run:
   ```
   python chess__game.py
   ```

### Build the exe yourself

```
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --add-data "stockfish.exe;." chess__game.py
```

The result is in `dist/`.

## Credits

- [Stockfish](https://stockfishchess.org/) powers the bot. It is open source under the GPL, and its source code is available on its website. The Stockfish binary is **not** committed to this repo.
- [python-chess](https://python-chess.readthedocs.io/) handles the rules and talks to Stockfish.
- [pygame-ce](https://pyga.me/) handles the window, drawing and input.
