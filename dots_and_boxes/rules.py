import re


def valid_move(board, orientation, row, col):
    """Return False rather than raising for malformed move arguments."""
    if orientation not in {"H", "V"}:
        return False
    # Reject bools too: bool is a subclass of int in Python.
    if type(row) is not int or type(col) is not int:
        return False
    if row < 0 or col < 0 or board.is_complete():
        return False
    if orientation == "H":
        return (row <= board.rows and col < board.cols
                and not board.horizontal[row][col])
    return (row < board.rows and col <= board.cols
            and not board.vertical[row][col])


def parse_move(raw, board):
    """Parse H/V row col or U. Coordinates must use ASCII decimal digits."""
    if not isinstance(raw, str) or len(raw) > 128:
        return None
    parts = raw.strip().upper().split()
    if parts == ["U"]:
        return ("U",)
    if len(parts) != 3 or parts[0] not in {"H", "V"}:
        return None
    # Full-match ASCII digits; str.isdigit() accepts superscripts and other
    # Unicode numerals that int() cannot necessarily parse.
    if not re.fullmatch(r"[0-9]{1,2}", parts[1]):
        return None
    if not re.fullmatch(r"[0-9]{1,2}", parts[2]):
        return None
    row, col = int(parts[1]), int(parts[2])
    if not valid_move(board, parts[0], row, col):
        return None
    return (parts[0], row, col)


def completed_boxes(board, before):
    return len(board.completed - before)
