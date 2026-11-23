"""Простое демо: только модели."""
import os
import sys
from datetime import datetime

# чтоб работало из любой папки
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cinema.models import Film, Viewer, Cashier, Cinema, Hall2D, IMAXHall, Session

film = Film("Дюна", "фантастика", 155, 12)
hall = Hall2D("Зал 1", 5, 10)
imax = IMAXHall("Аймакс", 6, 12)
ses = Session(film, imax, datetime(2026, 12, 1, 19, 30))

print(film)
print(hall.info(), "| цена:", hall.base_price())
print(imax.info(), "| цена:", imax.base_price())
print(ses.info(), "| цена билета:", ses.price())

vasya = Viewer("Вася", "vasya@mail.ru", 20)
ses.sell(5, vasya)
print("свободных мест:", len(ses.free_seats()))

cinema = Cinema()
cinema.add_hall(hall)
cinema.add_hall(imax)
print(cinema)
print(Cashier("Оля"))
