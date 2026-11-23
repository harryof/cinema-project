"""Продажа билетов."""
import logging

from src.cinema.models.ticket import Ticket
from src.cinema.exceptions import AgeLimitError

logger = logging.getLogger(__name__)


class SaleService:
    """Продаёт билеты, проверяет возраст и занятость мест."""

    def __init__(self, notifier=None):
        self.tickets = []
        self.notifier = notifier  # кому слать уведомления, можно None

    def sell(self, session, viewer, seat, cashier=None):
        """Продать билет, вернёт объект билета."""
        if viewer.age < session.film.age_rating:
            raise AgeLimitError(
                f"{viewer.name} ещё нет {session.film.age_rating} лет, нельзя на этот фильм"
            )
        session.sell(seat, viewer)  # если место занято, тут кинет ошибку
        t = Ticket(session, viewer, seat, session.price())
        self.tickets.append(t)
        if cashier is not None:
            cashier.sales += 1
        if self.notifier is not None:
            self.notifier.notify_all(f"Продан билет: {t}")
        logger.info("продан билет %s", t)
        return t

    def revenue(self):
        """Сколько всего заработали."""
        return sum(t.cost for t in self.tickets)
