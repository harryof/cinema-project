"""Бронирование мест."""
from src.cinema.exceptions import BookingError


class BookingService:
    """Бронирует места и даёт их выкупить."""

    def __init__(self):
        self.bookings = {}  # (id сеанса, место) -> зритель

    def book(self, session, viewer, seat):
        """Забронировать место."""
        session.book(seat, viewer)
        self.bookings[(session.id, seat)] = viewer

    def unbook(self, session, seat):
        """Снять бронь."""
        session.unbook(seat)
        self.bookings.pop((session.id, seat), None)

    def buy_booked(self, session, seat, sales):
        """Выкупить забронированное место через сервис продаж."""
        viewer = self.bookings.get((session.id, seat))
        if viewer is None:
            raise BookingError("такой брони нет")
        session.unbook(seat)
        del self.bookings[(session.id, seat)]
        return sales.sell(session, viewer, seat)
