class Board:
    """Board state for a rows-by-cols Dots and Boxes game."""

    def __init__(self, rows=2, cols=2):
        if type(rows) is not int or type(cols) is not int:
            raise ValueError("rows and cols must be integers")
        if not 1 <= rows <= 9 or not 1 <= cols <= 9:
            raise ValueError("rows and cols must be between 1 and 9")
        self.rows = rows
        self.cols = cols
        self.horizontal = [[False] * cols for _ in range(rows + 1)]
        self.vertical = [[False] * (cols + 1) for _ in range(rows)]
        self.completed = set()

    def add_line(self, orientation, row, col):
        """Add one legal line. Invalid calls leave the board unchanged."""
        # Local import avoids a module-level board/rules import cycle.
        from rules import valid_move
        if not valid_move(self, orientation, row, col):
            raise ValueError("invalid, out-of-range, or already-used move")
        if orientation == "H":
            self.horizontal[row][col] = True
        else:
            self.vertical[row][col] = True
        self._update_completed()

    def _update_completed(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (self.horizontal[r][c] and self.horizontal[r + 1][c]
                        and self.vertical[r][c] and self.vertical[r][c + 1]):
                    self.completed.add((r, c))

    def is_complete(self):
        total = self.rows * (self.cols + 1) + self.cols * (self.rows + 1)
        used = sum(sum(row) for row in self.horizontal)
        used += sum(sum(row) for row in self.vertical)
        return used == total

    def snapshot(self):
        """Return a deep-enough copy of all mutable game state."""
        return {
            "horizontal": [row[:] for row in self.horizontal],
            "vertical": [row[:] for row in self.vertical],
            "completed": set(self.completed),
        }

    def restore(self, state):
        """Restore a snapshot created by snapshot()."""
        self.horizontal = [row[:] for row in state["horizontal"]]
        self.vertical = [row[:] for row in state["vertical"]]
        self.completed = set(state["completed"])

    def display(self, scores, current):
        print()
        print(f"Scores: P1={scores[0]}  P2={scores[1]} | Turn: P{current + 1}")
        for r in range(self.rows + 1):
            pieces = ["."]
            for c in range(self.cols):
                pieces.append("---" if self.horizontal[r][c] else "   ")
                pieces.append(".")
            print("".join(pieces))
            if r < self.rows:
                middle = []
                for c in range(self.cols + 1):
                    middle.append("|" if self.vertical[r][c] else " ")
                    if c < self.cols:
                        middle.append(" " + ("X" if (r, c) in self.completed else " ") + " ")
                print("".join(middle))
        print()
