def choose_move(board):
    """Choose a legal move: take a box if possible, else avoid making 3 sides.

    If every available move gives away a box, choose the first legal move.
    The strategy is intentionally simple and deterministic.
    """
    from rules import valid_move

    candidates = []
    for r in range(board.rows + 1):
        for c in range(board.cols):
            if valid_move(board, "H", r, c):
                candidates.append(("H", r, c))
    for r in range(board.rows):
        for c in range(board.cols + 1):
            if valid_move(board, "V", r, c):
                candidates.append(("V", r, c))

    if not candidates:
        return None

    # Prefer a move that completes one or more boxes.
    for move in candidates:
        trial = _copy_board(board)
        trial.add_line(*move)
        if len(trial.completed) > len(board.completed):
            return move

    # Otherwise avoid any move that leaves an adjacent box with 3 sides.
    safe = []
    for move in candidates:
        trial = _copy_board(board)
        trial.add_line(*move)
        if not _creates_three_sided_box(trial):
            safe.append(move)
    return (safe or candidates)[0]


def _copy_board(board):
    clone = type(board)(board.rows, board.cols)
    clone.restore(board.snapshot())
    return clone


def _creates_three_sided_box(board):
    for r in range(board.rows):
        for c in range(board.cols):
            sides = (board.horizontal[r][c], board.horizontal[r + 1][c],
                     board.vertical[r][c], board.vertical[r][c + 1])
            if sum(sides) == 3:
                return True
    return False
