"""Тесты моделей."""
import pytest

from src.cinema.models import (
    Cinema, CinemaItem,
    Hall2D, Hall3D, IMAXHall, VIPHall, Session,
)
from src.cinema.exceptions import ValidationError, AlreadySoldError


def test_hall_prices():
    # у каждого зала своя цена
    assert Hall2D("a", 3, 10).base_price() == 300
    assert Hall3D("b", 3, 10).base_price() == 450
    assert IMAXHall("c", 3, 10).base_price() == 650
    assert VIPHall("d", 3, 10).base_price() == 900


def test_hall_capacity():
    hall = Hall2D("Зал 1", 5, 10)
    assert hall.capacity() == 50


def test_rows_validation():
    # слишком много рядов нельзя, дескриптор ругнётся
    with pytest.raises(ValidationError):
        Hall2D("Плохой", 100, 10)


def test_counter_grows():
    before = CinemaItem.total()
    Hall2D("x", 2, 5)
    Hall2D("y", 2, 5)
    assert CinemaItem.total() == before + 2


def test_ids_are_different():
    a = Hall2D("a", 2, 5)
    b = Hall2D("b", 2, 5)
    assert a.id != b.id
    assert a != b


def test_session_sell_and_free(session, viewer):
    session.sell(1, viewer)
    assert 1 not in session.free_seats()
    assert len(session.free_seats()) == session.hall.capacity() - 1


def test_double_sell_fails(session, viewer):
    session.sell(1, viewer)
    with pytest.raises(AlreadySoldError):
        session.sell(1, viewer)


def test_session_price_default(session):
    assert session.price() == 300


def test_session_to_from_dict(session):
    d = session.to_dict()
    back = Session.from_dict(d)
    assert back.film.title == session.film.title
    assert back.hall.name == session.hall.name
    assert type(back.hall) is type(session.hall)
    assert back.start == session.start
    assert back.id == session.id


def test_cinema_len():
    c = Cinema("Тест")
    c.add_hall(Hall2D("1", 2, 5))
    c.add_hall(Hall3D("2", 2, 5))
    assert len(c) == 2
