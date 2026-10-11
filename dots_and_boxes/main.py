import argparse

from game import DotsAndBoxes


def main():
    parser = argparse.ArgumentParser(description="Play Dots and Boxes.")
    parser.add_argument("--computer", action="store_true",
                        help="play against the computer as Player 1")
    parser.add_argument("--rows", type=int, default=2, choices=range(1, 10),
                        metavar="1-9", help="number of box rows (default: 2)")
    parser.add_argument("--cols", type=int, default=2, choices=range(1, 10),
                        metavar="1-9", help="number of box columns (default: 2)")
    args = parser.parse_args()
    DotsAndBoxes(rows=args.rows, cols=args.cols, computer=args.computer).run()


if __name__ == "__main__":
    main()
