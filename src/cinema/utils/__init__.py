"""Всякие мелкие помощники: дескриптор для проверки диапазона,
логирование, статик-утилиты."""

import logging
from datetime import datetime

from src.cinema.exceptions import ValidationError


class RangeCheck:
    """Дескриптор: число должно быть в пределах [lo, hi], иначе ошибка.

    Вешается на атрибут класса:
        class Hall:
            rows = RangeCheck(1, 30)
    """

    def __init__(self, lo: float, hi: float):
        self.lo = lo
        self.hi = hi
        self.name = ""  # заполнится в __set_name__

    def __set_name__(self, owner, name):
        # вызывается при создании класса, узнаём имя атрибута
        self.name = "_" + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if not (self.lo <= value <= self.hi):
            raise ValidationError(
                f"{self.name[1:]} должен быть от {self.lo} до {self.hi}, а не {value}")
        setattr(obj, self.name, value)


def setup_logging(level: str = "INFO") -> None:
    """Настройка логов, один раз на проект."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s")


class CinemaUtils:
    """Мелкие статические функции, классу нечего тут хранить."""

    @staticmethod
    def money(x: float) -> str:
        """45000 -> '45 000 ₽'."""
        return f"{x:,.0f} ₽".replace(",", " ")

    @staticmethod
    def parse_dt(s: str) -> datetime:
        """Строка -> datetime."""
        return datetime.fromisoformat(s)

    @staticmethod
    def is_weekend(dt: datetime) -> bool:
        return dt.weekday() >= 5  # сб=5, вс=6
