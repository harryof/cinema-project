"""Главный файл, запускает демо всех возможностей проекта."""
import os
from datetime import datetime

from config import CINEMA_NAME, DB_PATH
from src.cinema.models import Cinema, Viewer, Cashier, Ticket
from src.cinema.services import (
    SaleService, BookingService, TicketStorage, ReportService,
    NotificationService, EmailNotifier, SmsNotifier, StudentDiscount,
)
from src.cinema.patterns import (
    SessionFactory, CinemaRegistry, SessionAdapter,
    PopcornDecorator, PremiumSeatDecorator,
)
from src.cinema.database import DatabaseManager, SessionRepository, FilmRepository
from src.cinema.utils import setup_logging, CinemaUtils
from src.cinema.exceptions import CinemaError


def main():
    setup_logging()
    print(f"=== {CINEMA_NAME} ===\n")

    # фабрика делает залы и сеансы
    cinema = Cinema()
    ses1 = SessionFactory.make_session(
        "imax", "Аймакс", 5, 10, "Дюна", "фантастика", 155, 12,
        datetime(2026, 12, 1, 19, 30),
    )
    ses2 = SessionFactory.make_session(
        "2d", "Зал 2", 4, 8, "Холодное сердце", "мультик", 100, 0,
        datetime(2026, 12, 2, 11, 0), strategy=StudentDiscount(),
    )
    cinema.add_hall(ses1.hall)
    cinema.add_hall(ses2.hall)
    cinema.add_session(ses1)
    cinema.add_session(ses2)
    print(cinema)
    for s in cinema.sessions:
        print(" ", s.info(), "| цена:", CinemaUtils.money(s.price()))

    # синглтон: реестр кинотеатров один на всех
    reg = CinemaRegistry()
    reg.register("победа", cinema)
    print("\nв реестре:", CinemaRegistry().all().keys())

    # уведомления
    ns = NotificationService()
    ns.subscribe(EmailNotifier())
    ns.subscribe(SmsNotifier())

    # продажи
    print("\n--- продаём билеты ---")
    cashier = Cashier("Оля")
    sales = SaleService(notifier=ns)
    vasya = Viewer("Вася", "vasya@mail.ru", 20)
    petya = Viewer("Петя", "petya@mail.ru", 10)

    t1 = sales.sell(ses1, vasya, 7, cashier)
    sales.sell(ses1, Viewer("Маша", "", 25), 8, cashier)
    sales.sell(ses2, vasya, 1, cashier)

    # ошибки: возраст и занятое место
    try:
        sales.sell(ses1, petya, 9)  # Пете 10, а фильм 12+
    except CinemaError as e:
        print("поймали ошибку:", e)
    try:
        sales.sell(ses1, vasya, 7)  # место уже продано
    except CinemaError as e:
        print("поймали ошибку:", e)

    print(cashier)

    # бронь и выкуп брони
    print("\n--- бронь ---")
    booking = BookingService()
    booking.book(ses1, vasya, 10)
    print("свободных мест в аймаксе:", len(ses1.free_seats()))
    t_booked = booking.buy_booked(ses1, 10, sales)
    print("выкупили бронь:", t_booked)

    # декораторы: допы к билету
    print("\n--- допы к билету ---")
    fancy = PremiumSeatDecorator(PopcornDecorator(t1))
    print(fancy.sell(), "->", CinemaUtils.money(fancy.price()))

    # хранилище билетов
    storage = TicketStorage()
    for t in sales.tickets:
        storage.add(t)
    print("\nв хранилище билетов:", len(storage))

    # адаптер: сеанс от внешней системы
    print("\n--- сеанс от внешней системы ---")
    external = {
        "movie": "Аватар 3",
        "hall_kind": "standard",
        "hall_name": "Зал 3",
        "rows": 6,
        "seats": 12,
        "time": "2026-12-05T20:00:00",
        "genre": "фантастика",
        "duration": 180,
        "age": 12,
    }
    ses3 = SessionAdapter.to_session(external)
    cinema.add_session(ses3)
    print(ses3.info())

    # отчёты
    print("\n--- отчёт ---")
    rep = ReportService(sales)
    print("выручка по фильмам:", rep.revenue_by_film())
    print("заполняемость:", rep.occupancy())
    print("топ фильмов:", rep.top_films())
    print("всего заработали:", CinemaUtils.money(sales.revenue()))

    # база данных
    print("\n--- база данных ---")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)  # чтоб демо всегда с чистого листа
    with DatabaseManager() as db:
        db.init_db()
        repo = SessionRepository(db)
        for s in cinema.sessions:
            repo.save(s)
        print("сеансов в базе:", len(repo.all()))
        back = repo.all()[0]
        print("достали из базы:", back.info())
        FilmRepository(db).save(ses1.film)
        print("фильмов в базе:", len(FilmRepository(db).all()))

    print("\nвсё отработало!")


if __name__ == "__main__":
    main()
