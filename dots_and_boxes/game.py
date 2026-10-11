from board import Board
from rules import parse_move, completed_boxes
from ai import choose_move


class DotsAndBoxes:
    def __init__(self, rows=2, cols=2, computer=False):
        self.board = Board(rows, cols)
        self.current = 0
        self.scores = [0, 0]
        self.computer = computer
        # Each entry restores the state before a human move. In computer
        # mode this includes the computer's reply, so U undoes the whole turn.
        self.history = []

    def _save_state(self):
        self.history.append({
            "board": self.board.snapshot(),
            "scores": self.scores[:],
            "current": self.current,
        })

    def undo(self):
        if not self.history:
            return False
        state = self.history.pop()
        self.board.restore(state["board"])
        self.scores = state["scores"][:]
        self.current = state["current"]
        return True

    def _apply_move(self, move):
        orientation, row, col = move
        before = set(self.board.completed)
        self.board.add_line(orientation, row, col)
        newly_completed = completed_boxes(self.board, before)
        self.scores[self.current] += newly_completed
        if not newly_completed:
            self.current = 1 - self.current
        return newly_completed

    def run(self):
        print("Dots and Boxes")
        print("Enter H row col, V row col, or U to undo. Coordinates start at 0.")
        print("Example: H 0 1")
        if self.computer:
            print("Computer mode: you are Player 1.")
        try:
            while not self.board.is_complete():
                # Computer is player index 1; it acts automatically.
                if self.computer and self.current == 1:
                    self.board.display(self.scores, self.current)
                    move = choose_move(self.board)
                    if move is None:
                        break
                    got = self._apply_move(move)
                    print(f"Computer plays {move[0]} {move[1]} {move[2]}.")
                    if got:
                        print(f"Computer completed {got} box(es) and plays again.")
                    continue

                self.board.display(self.scores, self.current)
                try:
                    raw = input(f"Player {self.current + 1}, move: ")
                except (EOFError, KeyboardInterrupt):
                    print("\nGame ended.")
                    return

                move = parse_move(raw, self.board)
                if move == ("U",):
                    if self.undo():
                        print("Undid the previous move.")
                    else:
                        print("Nothing to undo.")
                    continue
                if move is None:
                    print("Invalid command or move; try again.")
                    continue

                # Save before each human move. The AI reply, if any, happens
                # before the next prompt, so undo restores the pre-human state.
                self._save_state()
                got = self._apply_move(move)
                if got:
                    print(f"Player {self.current + 1} completed {got} box(es) and plays again.")
                if self.computer and self.current == 1:
                    # Keep the state before the human move on the stack; AI
                    # state changes are undone together with this human move.
                    pass

        except KeyboardInterrupt:
            print("\nGame ended.")
            return

        self.board.display(self.scores, self.current)
        print("Game over!")
        if self.scores[0] == self.scores[1]:
            print("The game is a draw.")
        else:
            winner = 1 if self.scores[0] > self.scores[1] else 2
            print(f"Player {winner} wins!")
