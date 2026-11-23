"""Что делают команды из командной строки."""
from datetime import datetime

from src.cinema.models import Viewer
from src.cinema.services import SaleService
from src.cinema.patterns import SessionFactory
from src.cinema.database import DatabaseManager, SessionRepository, ViewerRepository


def cmd_add_hall(db, args):
    """Добавить зал в базу."""
    hall = SessionFactory.make_hall(args.type, args.name, args.rows, args.seats)
    db.execute(
        "INSERT INTO halls (name, type, rows, seats_in_row) VALUES (?, ?, ?, ?)",
        (hall.name, type(hall).__name__, hall.rows, hall.seats_in_row),
    )
    print(f"добавили зал: {hall.info()}")


def cmd_add_session(db, args):
    """Добавить сеанс в базу."""
    if args.start:
        start = datetime.strptime(args.start, "%Y-%m-%d %H:%M")
    else:
        start = datetime.now()
    ses = SessionFactory.make_session(
        args.hall_type, args.hall_name, args.rows, args.seats,
        args.film, args.genre, args.duration, args.age, start,
    )
    sid = SessionRepository(db).save(ses)
    print(f"добавили сеанс #{sid}: {ses.info()}")


def _load_session(db, session_id):
    """Достаёт сеанс из базы и подгружает уже проданные места."""
    ses = SessionRepository(db).get(session_id)
    if ses is None:
        return None
    rows = db.fetch_all("SELECT seat FROM tickets WHERE session_id = ?", (session_id,))
    for r in rows:
        ses.sold[r["seat"]] = None
    return ses


def cmd_sell(db, args):
    """Продать билет."""
    ses = _load_session(db, args.session_id)
    if ses is None:
        print(f"нет сеанса с id {args.session_id}")
        return
    viewer = Viewer(args.name, "", args.age)
    sales = SaleService()
    try:
        t = sales.sell(ses, viewer, args.seat)
    except Exception as e:
        print(f"не получилось: {e}")
        return
    viewer_id = ViewerRepository(db).save(viewer)
    db.execute(
        "INSERT INTO tickets (session_id, viewer_id, seat, cost) VALUES (?, ?, ?, ?)",
        (args.session_id, viewer_id, t.seat, t.cost),
    )
    print(f"продали: {t}")


def cmd_book(db, args):
    """Забронировать место (бронь живёт, пока работает программа)."""
    ses = _load_session(db, args.session_id)
    if ses is None:
        print(f"нет сеанса с id {args.session_id}")
        return
    try:
        ses.book(args.seat, args.name)
    except Exception as e:
        print(f"не получилось: {e}")
        return
    print(f"место {args.seat} забронировано на {args.name}")


def cmd_report(db, args):
    """Отчёт по продажам."""
    rows = db.fetch_all(
        """SELECT f.title, COUNT(*) AS cnt, SUM(t.cost) AS total
           FROM tickets t
           JOIN sessions s ON s.id = t.session_id
           JOIN films f ON f.id = s.film_id
           GROUP BY f.title"""
    )
    print("Отчёт по продажам:")
    total = 0
    for r in rows:
        print(f"  {r['title']}: {r['cnt']} билетов, {r['total']} руб.")
        total += r["total"] or 0
    print(f"Итого: {total} руб.")


def cmd_list(db, args):
    """Показать все сеансы."""
    sessions = SessionRepository(db).all()
    if not sessions:
        print("сеансов пока нет")
    for s in sessions:
        print(f"#{s.id} {s.info()}")


def run(args):
    """Запускает нужную команду."""
    cmds = {
        "add-hall": cmd_add_hall,
        "add-session": cmd_add_session,
        "sell": cmd_sell,
        "book": cmd_book,
        "report": cmd_report,
        "list": cmd_list,
    }
    if args.command not in cmds:
        print("напиши команду, например: python -m src.cinema.cli list")
        return
    with DatabaseManager() as db:
        db.init_db()
        cmds[args.command](db, args)
