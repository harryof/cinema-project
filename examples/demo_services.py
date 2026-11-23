"""Демо сервисов: продажи, бронь, уведомления, отчёты."""
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cinema.models import Film, Viewer, Cashier, Hall2D, Session
from src.cinema.services import (
    SaleService, BookingService, ReportService,
    NotificationService, EmailNotifier, MorningDiscount,
)
from src.cinema.exceptions import CinemaError

ns = NotificationService()
ns.subscribe(EmailNotifier())

ses = Session(
    Film("Дюна", "фантастика", 155, 12),
    Hall2D("Зал 1", 5, 10),
    datetime(2026, 12, 1, 10, 0),
    price_strategy=MorningDiscount(),  # утром дешевле
)
print("цена на утренний сеанс:", ses.price())

cashier = Cashier("Оля")
sales = SaleService(notifier=ns)
vasya = Viewer("Вася", "", 20)

sales.sell(ses, vasya, 1, cashier)
sales.sell(ses, vasya, 2, cashier)

# ребёнка на взрослый фильм не пустим
ses18 = Session(Film("Ужасы", "хоррор", 90, 18), Hall2D("Зал 2", 3, 6),
                datetime(2026, 12, 1, 22, 0))
try:
    sales.sell(ses18, Viewer("Петя", "", 10), 1)
except CinemaError as e:
    print("не пустили:", e)

booking = BookingService()
booking.book(ses, vasya, 9)
booking.buy_booked(ses, 9, sales)

rep = ReportService(sales)
print("выручка:", rep.revenue_by_film())
print("топ:", rep.top_films())
print(cashier)
