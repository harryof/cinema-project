"""Полное демо: модели, сервисы, паттерны и база."""
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cinema.models import Viewer, Cashier
from src.cinema.services import SaleService, ReportService, TicketStorage
from src.cinema.patterns import (
    SessionFactory, CinemaRegistry, SessionAdapter, PopcornDecorator,
)
from src.cinema.database import DatabaseManager, SessionRepository

# фабрика
ses = SessionFactory.make_session(
    "vip", "Вип зал", 3, 8, "Дюна", "фантастика", 155, 12,
    datetime(2026, 12, 1, 19, 30),
)
print(ses.info(), "| цена:", ses.price())

# синглтон
reg = CinemaRegistry()
reg.register("главный", ses)
print("реестр тот же самый:", reg is CinemaRegistry())

# продажа + декоратор
sales = SaleService()
t = sales.sell(ses, Viewer("Вася", "", 20), 3, Cashier("Оля"))
with_popcorn = PopcornDecorator(t)
print(with_popcorn.sell(), "->", with_popcorn.price(), "руб.")

# хранилище
storage = TicketStorage()
tid = storage.add(t)
print("достали из хранилища:", storage[tid])

# адаптер
external = {
    "movie": "Аватар 3", "hall_kind": "imax", "hall_name": "Аймакс",
    "rows": 5, "seats": 10, "time": "2026-12-05T20:00:00",
}
ses2 = SessionAdapter.to_session(external)
print("из внешней системы:", ses2.info())

# база
db_path = "demo_full.db"
if os.path.exists(db_path):
    os.remove(db_path)
with DatabaseManager(db_path) as db:
    db.init_db()
    repo = SessionRepository(db)
    repo.save(ses)
    repo.save(ses2)
    print("сеансов в базе:", len(repo.all()))
os.remove(db_path)  # прибираемся за собой

print("отчёт:", ReportService(sales).revenue_by_film())
