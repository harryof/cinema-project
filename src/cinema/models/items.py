"""Базовый класс и залы кинотеатра."""
from abc import ABC

from config import MIN_ROWS, MAX_ROWS, MIN_SEATS, MAX_SEATS
from src.cinema.interfaces import Infoable, Describable
from src.cinema.utils import RangeCheck


class CinemaItem(ABC):
    """Базовый класс для всего в кинотеатре, у каждого объекта свой id."""

    _count = 0

    def __init__(self):
        CinemaItem._count += 1
        self.id = CinemaItem._count

    @classmethod
    def total(cls):
        """Сколько всего объектов создали."""
        return cls._count


class Hall(CinemaItem, Infoable, Describable):
    """Обычный зал, от него наследуются остальные."""

    rows = RangeCheck(MIN_ROWS, MAX_ROWS)
    seats_in_row = RangeCheck(MIN_SEATS, MAX_SEATS)

    def __init__(self, name, rows, seats_in_row):
        super().__init__()
        self.name = name
        self.rows = rows
        self.seats_in_row = seats_in_row

    def capacity(self):
        """Сколько всего мест в зале."""
        return self.rows * self.seats_in_row

    def base_price(self):
        """Базовая цена билета, у каждого зала своя."""
        return 300

    def info(self):
        """Коротко про зал."""
        return f"Зал '{self.name}', мест: {self.capacity()}"

    def describe(self):
        """Всё про зал в виде словаря."""
        return {
            "id": self.id,
            "name": self.name,
            "type": type(self).__name__,
            "rows": self.rows,
            "seats_in_row": self.seats_in_row,
            "capacity": self.capacity(),
            "base_price": self.base_price(),
        }

    def __str__(self):
        return self.info()

    def __eq__(self, other):
        return isinstance(other, Hall) and self.id == other.id


class Hall2D(Hall):
    """Простой зал."""

    def base_price(self):
        return 300


class Hall3D(Hall):
    """Зал с 3D, подороже."""

    def base_price(self):
        return 450


class IMAXHall(Hall):
    """Аймакс, экран огромный."""

    def base_price(self):
        return 650


class VIPHall(Hall):
    """Вип зал с диванами."""

    def base_price(self):
        return 900
