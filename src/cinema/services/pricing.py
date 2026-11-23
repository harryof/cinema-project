"""Стратегии цены на билеты."""
from abc import ABC, abstractmethod
from datetime import datetime

from config import WEEKEND_EXTRA
from src.cinema.utils import CinemaUtils


class PriceStrategy(ABC):
    """Базовая стратегия, от неё наследуются остальные."""

    @abstractmethod
    def calc(self, base):
        """Считает цену от базовой цены зала."""


class FlatPrice(PriceStrategy):
    """Обычная цена, без скидок и наценок."""

    def calc(self, base):
        return base


class StudentDiscount(PriceStrategy):
    """Студентам дешевле на 30%."""

    def calc(self, base):
        return base * 0.7


class WeekendPrice(PriceStrategy):
    """В выходные дороже."""

    def calc(self, base, day=None):
        # если день не передали, берём сегодня
        day = day or datetime.now()
        if CinemaUtils.is_weekend(day):
            return base * (1 + WEEKEND_EXTRA)
        return base


class MorningDiscount(PriceStrategy):
    """Утренние сеансы дешевле на 25%."""

    def calc(self, base, when=None):
        when = when or datetime.now()
        if when.hour < 12:
            return base * 0.75
        return base
