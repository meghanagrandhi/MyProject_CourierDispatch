import unittest

from board import Board
from rules import valid_move, parse_move, completed_boxes
from game import DotsAndBoxes
from ai import choose_move


class TestDotsAndBoxes(unittest.TestCase):
    def test_valid_horizontal_move(self):
        board = Board()
        self.assertTrue(valid_move(board, "H", 0, 0))
        board.add_line("H", 0, 0)
        self.assertTrue(board.horizontal[0][0])

    def test_valid_vertical_move(self):
        board = Board()
        self.assertTrue(valid_move(board, "V", 0, 0))
        board.add_line("V", 0, 0)
        self.assertTrue(board.vertical[0][0])

    def test_invalid_and_repeated_move_do_not_change_state(self):
        board = Board()
        board.add_line("H", 0, 0)
        before = board.snapshot()
        self.assertFalse(valid_move(board, "H", 0, 0))
        self.assertFalse(valid_move(board, "H", -1, 0))
        with self.assertRaises(ValueError):
            board.add_line("H", 0, 0)
        self.assertEqual(board.snapshot(), before)

    def test_completion_of_one_box(self):
        board = Board(1, 1)
        for move in [("H", 0, 0), ("H", 1, 0), ("V", 0, 0)]:
            board.add_line(*move)
        before = set(board.completed)
        board.add_line("V", 0, 1)
        self.assertEqual(completed_boxes(board, before), 1)
        game = DotsAndBoxes(1, 1)
        for move in [("H", 0, 0), ("H", 1, 0), ("V", 0, 0)]:
            game._apply_move(move)
        game.current = 0
        got = game._apply_move(("V", 0, 1))
        self.assertEqual(got, 1)
        self.assertEqual(game.scores[0], 1)
        self.assertEqual(game.current, 0)

    def test_completes_two_boxes_at_once(self):
        board = Board(1, 2)
        # Complete both boxes with the final vertical edge shared by neither;
        # set up all other edges first.
        for move in [("H", 0, 0), ("H", 0, 1),
                     ("H", 1, 0), ("H", 1, 1),
                     ("V", 0, 0), ("V", 0, 2)]:
            board.add_line(*move)
        before = set(board.completed)
        board.add_line("V", 0, 1)
        self.assertEqual(completed_boxes(board, before), 2)

    def test_end_of_game_and_no_moves_after_game_over(self):
        board = Board(1, 1)
        for move in [("H", 0, 0), ("H", 1, 0),
                     ("V", 0, 0), ("V", 0, 1)]:
            board.add_line(*move)
        self.assertTrue(board.is_complete())
        self.assertFalse(valid_move(board, "H", 0, 0))
        before = board.snapshot()
        with self.assertRaises(ValueError):
            board.add_line("H", 0, 0)
        self.assertEqual(board.snapshot(), before)

    def test_malformed_input(self):
        board = Board()
        for raw in ["", "H 0", "X 0 0", "H -1 0", "H 0 999999999999999999",
                    "H 0 ²", "H ٠ 0", "H 0 0 extra", "H 0 0" + " " * 200]:
            self.assertIsNone(parse_move(raw, board), raw)

    def test_undo_restores_board_score_and_turn(self):
        game = DotsAndBoxes(1, 1)
        game._save_state()
        game._apply_move(("H", 0, 0))
        game.scores[0] = 5
        game.current = 1
        self.assertTrue(game.undo())
        self.assertEqual(game.scores, [0, 0])
        self.assertEqual(game.current, 0)
        self.assertFalse(game.board.horizontal[0][0])

    def test_computer_prefers_completing_box(self):
        board = Board(1, 1)
        for move in [("H", 0, 0), ("H", 1, 0), ("V", 0, 0)]:
            board.add_line(*move)
        self.assertEqual(choose_move(board), ("V", 0, 1))

    def test_board_size_validation(self):
        for rows, cols in [(0, 2), (2, 10), (-1, 1)]:
            with self.assertRaises(ValueError):
                Board(rows, cols)


if __name__ == "__main__":
    unittest.main()
