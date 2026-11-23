"""Свои исключения, чтобы отличать наши ошибки от обычных питоновских."""


class CinemaError(Exception):
    """Базовое исключение проекта, все остальные от него."""


class NotFoundError(CinemaError):
    """Когда сеанс/зритель/билет не нашли."""


class AlreadySoldError(CinemaError):
    """Место уже продано."""


class BookingError(CinemaError):
    """Что-то не так с бронью."""


class AgeLimitError(CinemaError):
    """Зритель не проходит по возрастному рейтингу."""


class ValidationError(CinemaError):
    """Кривые данные (отрицательная цена и т.п.)."""


class DatabaseError(CinemaError):
    """Ошибка при работе с базой."""
