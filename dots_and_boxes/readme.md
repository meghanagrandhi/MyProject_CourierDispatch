# Lab 4: Vibe Coding, Dots and Boxes

**Name:** Meghana Grandhi  **SRN:** PES1UG24CS268  **Section:** E
**Original repo:** https://github.com/SETAPESU26/23_dots_and_boxes (no pull request raised)
**AI tool used:** ChatGPT  **Prompts used:** 3

## Contents
| File | Purpose |
|---|---|
| board.py, rules.py, game.py, main.py | Updated modular game code |
| ai.py | New computer opponent |
| test_dots_and_boxes.py | Automated unittest tests |
| CHANGES.md | Bugs fixed, features added, design decisions |
| before.mp4 | 10-second demo of the original game |
| after.mp4 | 10-second demo of the fixed game |
| Chat_History.pdf | Exported AI conversation |

## Bugs found in the original (shown in before.mp4)
1. **Board drawing:** the corner dots are missing, so the board is hard to read.
2. **Crash on invalid input:** typing `H 0 ²` raises
   `ValueError: invalid literal for int() with base 10`, and the game exits
   with a traceback.

**Checked and found correct:** score and turn handling. A move that completes
two boxes awards 2 points and keeps the turn. I kept this as a regression test
and did not count it as a bug.

## Features added
- Computer opponent: `python main.py --computer`
- Undo: type `U` to restore the board, score and turn (in computer mode it
  goes back to before my last move)
- Board size: `--rows` and `--cols` (1 to 9)
- Stronger validation: malformed, negative, huge and non-ASCII input are
  rejected; moves after game over are blocked

## How to run
```
python main.py                         # original 2x2, two players
python main.py --computer              # play the computer
python main.py --rows 3 --cols 5       # custom board
python -m unittest -v test_dots_and_boxes.py
```
Moves look like `H 0 1` or `V 1 0`. `U` undoes the last move.

## Demo
**before.mp4** (original game, `python main.py`):
the board is shown without corner dots. Moves `H 0 0` and `V 0 1` are played,
then `H 0 ²` crashes the game with a ValueError traceback.

**after.mp4** (fixed game, `python main.py --computer`):
the board shows all dots. After `H 0 0`, the computer replies `H 0 1`.
`H 0 ²` is rejected with "Invalid command or move; try again" and the game
continues. `U` prints "Undid the previous move" and restores the empty board.

## Test results
10 tests pass: horizontal and vertical moves, repeated move, box completion,
two boxes at once, game over, malformed input, undo, computer player.
