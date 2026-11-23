"""Командная строка через argparse."""
import argparse


def make_parser():
    """Собирает парсер со всеми командами."""
    p = argparse.ArgumentParser(prog="cinema", description="Кинотеатр: сеансы и билеты")
    sub = p.add_subparsers(dest="command")

    a = sub.add_parser("add-hall", help="добавить зал")
    a.add_argument("type", choices=["2d", "3d", "imax", "vip"])
    a.add_argument("name")
    a.add_argument("--rows", type=int, default=5)
    a.add_argument("--seats", type=int, default=10)

    a = sub.add_parser("add-session", help="добавить сеанс")
    a.add_argument("film")
    a.add_argument("--genre", default="драма")
    a.add_argument("--duration", type=int, default=120)
    a.add_argument("--age", type=int, default=12)
    a.add_argument("--hall-type", default="2d", choices=["2d", "3d", "imax", "vip"])
    a.add_argument("--hall-name", default="Зал 1")
    a.add_argument("--rows", type=int, default=5)
    a.add_argument("--seats", type=int, default=10)
    a.add_argument("--start", default=None, help="дата и время, напр. 2026-12-01 19:30")

    a = sub.add_parser("sell", help="продать билет")
    a.add_argument("session_id", type=int)
    a.add_argument("seat", type=int)
    a.add_argument("--name", default="Гость")
    a.add_argument("--age", type=int, default=18)

    a = sub.add_parser("book", help="забронировать место")
    a.add_argument("session_id", type=int)
    a.add_argument("seat", type=int)
    a.add_argument("--name", default="Гость")
    a.add_argument("--age", type=int, default=18)

    sub.add_parser("report", help="отчёт по продажам")
    sub.add_parser("list", help="список сеансов")

    return p
