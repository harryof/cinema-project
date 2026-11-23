"""Сеанс: какой фильм, в каком зале и когда."""
from datetime import datetime

from src.cinema.interfaces import Infoable, Describable, Sellable, Bookable
from src.cinema.models.items import CinemaItem
from src.cinema.models.film import Film
from src.cinema.models import items as hall_types
from src.cinema.exceptions import AlreadySoldError, BookingError


class Session(CinemaItem, Infoable, Describable, Sellable, Bookable):
    """Сеанс, тут продают и бронируют места."""

    def __init__(self, film, hall, start, price_strategy=None):
        super().__init__()
        self.film = film
        self.hall = hall
        self.start = start
        self.price_strategy = price_strategy  # если None, просто цена зала
        self.sold = {}    # место -> зритель
        self.booked = {}  # место -> кто забронировал

    def price(self):
        """Цена билета на этот сеанс."""
        if self.price_strategy is None:
            return self.hall.base_price()
        return self.price_strategy.calc(self.hall.base_price())

    def sell(self, seat, viewer=None):
        """Продать место, если занято - кидаем ошибку."""
        if seat in self.sold or seat in self.booked:
            raise AlreadySoldError(f"место {seat} уже занято")
        if seat < 1 or seat > self.hall.capacity():
            raise BookingError(f"места {seat} нет в зале")
        self.sold[seat] = viewer

    def book(self, seat, viewer=None):
        """Забронировать место."""
        if seat in self.sold or seat in self.booked:
            raise BookingError(f"место {seat} уже занято")
        self.booked[seat] = viewer

    def unbook(self, seat):
        """Снять бронь."""
        if seat not in self.booked:
            raise BookingError(f"место {seat} не было забронировано")
        del self.booked[seat]

    def free_seats(self):
        """Какие места ещё свободны."""
        busy = set(self.sold) | set(self.booked)
        return [s for s in range(1, self.hall.capacity() + 1) if s not in busy]

    def info(self):
        """Коротко про сеанс."""
        return f"Сеанс '{self.film.title}' в зале '{self.hall.name}', {self.start:%d.%m %H:%M}"

    def describe(self):
        """Всё про сеанс словарём."""
        return {
            "id": self.id,
            "film": self.film.title,
            "hall": self.hall.name,
            "start": self.start.isoformat(),
            "price": self.price(),
            "sold": len(self.sold),
            "booked": len(self.booked),
            "free": len(self.free_seats()),
        }

    def to_dict(self):
        """В словарь, чтоб в базу положить."""
        return {
            "id": self.id,
            "film_title": self.film.title,
            "film_genre": self.film.genre,
            "film_duration": self.film.duration,
            "film_age": self.film.age_rating,
            "hall_name": self.hall.name,
            "hall_type": type(self.hall).__name__,
            "hall_rows": self.hall.rows,
            "hall_seats": self.hall.seats_in_row,
            "start": self.start.isoformat(),
        }

    @staticmethod
    def from_dict(d):
        """Обратно из словаря."""
        hall_cls = getattr(hall_types, d["hall_type"])
        hall = hall_cls(d["hall_name"], d["hall_rows"], d["hall_seats"])
        film = Film(d["film_title"], d["film_genre"], d["film_duration"], d["film_age"])
        ses = Session(film, hall, datetime.fromisoformat(d["start"]))
        ses.id = d["id"]  # чтоб айдишник совпадал с базой
        return ses

    def __str__(self):
        return self.info()
