"""Декораторы для билета: допы типа попкорна и парковки."""
from src.cinema.interfaces import Sellable


class TicketDecorator(Sellable):
    """Обертка над билетом или над другим декоратором."""

    def __init__(self, item):
        self.item = item

    def price(self):
        return self.item.price()

    def sell(self):
        return self.item.sell()


class PopcornDecorator(TicketDecorator):
    """Билет + попкорн."""

    def price(self):
        return self.item.price() + 250

    def sell(self):
        return self.item.sell() + " + попкорн"


class ParkingDecorator(TicketDecorator):
    """Билет + парковка."""

    def price(self):
        return self.item.price() + 150

    def sell(self):
        return self.item.sell() + " + парковка"


class PremiumSeatDecorator(TicketDecorator):
    """Премиум место, в полтора раза дороже."""

    def price(self):
        return self.item.price() * 1.5

    def sell(self):
        return self.item.sell() + " (премиум место)"
