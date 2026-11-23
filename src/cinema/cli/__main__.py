"""Чтоб работало python -m src.cinema.cli."""
from src.cinema.cli.parser import make_parser
from src.cinema.cli.commands import run

if __name__ == "__main__":
    args = make_parser().parse_args()
    run(args)
