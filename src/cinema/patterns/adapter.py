"""Адаптер: делает наш сеанс из словаря чужой системы."""
from datetime import datetime

from src.cinema.patterns.factory import SessionFactory


class SessionAdapter:
    """Переделывает словарь от внешней системы в наш сеанс."""

    # как у них называется -> наш тип зала
    HALL_MAP = {
        "standard": "2d",
        "3d": "3d",
        "imax": "imax",
        "vip": "vip",
    }

    @staticmethod
    def to_session(external):
        """external - словарь вида {'movie': ..., 'hall_kind': ..., 'time': ...}."""
        hall_type = SessionAdapter.HALL_MAP.get(external["hall_kind"], "2d")
        return SessionFactory.make_session(
            hall_type=hall_type,
            hall_name=external["hall_name"],
            rows=external["rows"],
            seats=external["seats"],
            film_title=external["movie"],
            genre=external.get("genre", "неизвестно"),
            duration=external.get("duration", 90),
            age=external.get("age", 0),
            start=datetime.fromisoformat(external["time"]),
        )
