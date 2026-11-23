"""Фабрика сеансов: сама подбирает тип зала по строке."""
from src.cinema.models import Film, Session, Hall2D, Hall3D, IMAXHall, VIPHall


class SessionFactory:
    """Делает залы и сеансы, чтоб не собирать всё руками."""

    HALLS = {
        "2d": Hall2D,
        "3d": Hall3D,
        "imax": IMAXHall,
        "vip": VIPHall,
    }

    @classmethod
    def make_hall(cls, hall_type, name, rows, seats_in_row):
        """Сделать зал нужного типа."""
        if hall_type not in cls.HALLS:
            raise ValueError(f"не знаю такой тип зала: {hall_type}")
        return cls.HALLS[hall_type](name, rows, seats_in_row)

    @classmethod
    def make_session(cls, hall_type, hall_name, rows, seats,
                     film_title, genre, duration, age, start, strategy=None):
        """Сразу готовый сеанс с фильмом и залом."""
        hall = cls.make_hall(hall_type, hall_name, rows, seats)
        film = Film(film_title, genre, duration, age)
        return Session(film, hall, start, strategy)
