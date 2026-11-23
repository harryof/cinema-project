"""Зритель и кассир."""
from dataclasses import dataclass


@dataclass
class Viewer:
    """Зритель: имя, почта и возраст (возраст нужен для рейтинга фильма)."""

    name: str
    email: str
    age: int

    def __str__(self):
        return f"{self.name}, {self.age} лет"


@dataclass
class Cashier:
    """Кассир, считает сколько билетов продал."""

    name: str
    sales: int = 0

    def __str__(self):
        return f"кассир {self.name}, продал: {self.sales}"
