"""Тесты паттернов."""
from datetime import datetime

import pytest

from src.cinema.models import Film, Viewer, Hall2D, IMAXHall, Session, Ticket
from src.cinema.patterns import (
    SessionFactory, CinemaRegistry, SessionAdapter,
    PopcornDecorator, ParkingDecorator, PremiumSeatDecorator,
)


def make_ticket():
    ses = Session(Film("Дюна", "фантастика", 155, 12),
                  Hall2D("Зал 1", 5, 10), datetime(2026, 12, 1, 19, 30))
    return Ticket(ses, Viewer("Вася", "", 20), 7, 300)


def test_singleton_same_object():
    a = CinemaRegistry()
    b = CinemaRegistry()
    assert a is b  # это один и тот же объект


def test_singleton_register():
    reg = CinemaRegistry()
    reg.register("победа", "кинотеатр1")
    assert CinemaRegistry().get("победа") == "кинотеатр1"


def test_factory_halls():
    hall = SessionFactory.make_hall("imax", "Аймакс", 5, 10)
    assert isinstance(hall, IMAXHall)
    with pytest.raises(ValueError):
        SessionFactory.make_hall("8d", "Чудо-зал", 5, 10)


def test_factory_session():
    ses = SessionFactory.make_session(
        "vip", "Вип", 3, 8, "Дюна", "фантастика", 155, 12,
        datetime(2026, 12, 1, 19, 30),
    )
    assert ses.film.title == "Дюна"
    assert ses.hall.base_price() == 900


def test_decorators_price():
    t = make_ticket()
    assert t.price() == 300
    assert PopcornDecorator(t).price() == 550
    assert ParkingDecorator(PopcornDecorator(t)).price() == 700
    assert PremiumSeatDecorator(t).price() == 450


def test_decorators_text():
    t = make_ticket()
    s = PopcornDecorator(t).sell()
    assert "попкорн" in s


def test_adapter():
    external = {
        "movie": "Дюна",
        "hall_kind": "imax",
        "hall_name": "Аймакс",
        "rows": 5,
        "seats": 10,
        "time": "2026-12-01T19:30:00",
        "genre": "фантастика",
        "duration": 155,
        "age": 12,
    }
    ses = SessionAdapter.to_session(external)
    assert ses.film.title == "Дюна"
    assert isinstance(ses.hall, IMAXHall)
    assert ses.start == datetime(2026, 12, 1, 19, 30)
