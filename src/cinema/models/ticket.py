"""Билет на сеанс."""
from dataclasses import dataclass

from src.cinema.interfaces import Sellable


@dataclass
class Ticket(Sellable):
    """Билет: сеанс, кто купил, место и цена."""

    session: object
    viewer: object
    seat: int
    cost: float

    def price(self):
        """Цена билета, нужно для декораторов."""
        return self.cost

    def sell(self):
        """Что пишем при продаже."""
        return f"место {self.seat} на '{self.session.film.title}'"

    def __str__(self):
        return f"Билет: {self.session.film.title}, место {self.seat}, {self.cost} руб."
