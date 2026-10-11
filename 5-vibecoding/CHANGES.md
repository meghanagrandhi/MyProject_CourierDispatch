# Changes

## Bugs fixed
- Box completion is calculated from the set difference between completed boxes before and after a move. A move can therefore score one or two boxes, and the score increases by the exact number.
- Turn changes only when a move does not complete a box. Completing one or more boxes lets the same player move again.
- Board drawing now prints a dot at every corner and intersection and keeps rows aligned for rectangular boards.
- `rules.py` validates orientation, integer coordinates, bounds, repeated edges, and game-over state before a move is accepted. `Board.add_line()` independently rejects illegal moves, so callers cannot silently corrupt the board.
- Input parsing uses ASCII decimal digits and caps command length. Superscript digits such as `²`, non-ASCII numerals, negative coordinates, enormous coordinates, malformed commands, and extra tokens are rejected without changing state.
- EOF (`Ctrl+D` on Unix-like systems) and Ctrl+C end the interactive game cleanly.

## Features
- `python main.py --computer` starts a single-player game with the human as Player 1.
- New `ai.py` chooses a move that completes a box when possible. Otherwise it prefers moves that do not leave a box with three sides; if no safe move exists, it chooses a legal move.
- `U` undoes the last human move. In computer mode, the snapshot is taken before the human move, so undo also removes the computer's reply.
- `--rows` and `--cols` configure a board from 1 to 9 boxes in each dimension. Defaults remain 2 by 2.
- Added standard-library `unittest` coverage in `test_dots_and_boxes.py`.

## Design decisions
- Kept `board.py`, `rules.py`, `game.py`, and `main.py` separate; AI strategy lives in `ai.py`.
- The board owns its edge and completed-box state. Rules validate and parse moves. The game owns score, turn, history, and command-loop behaviour.
- Undo snapshots copy all mutable board data, score, and current player. This makes undo restore the complete game state rather than just removing an edge.
- The AI is a simple rule-based opponent, not a search-based or guaranteed-optimal player.
- Only Python's standard library is used.
