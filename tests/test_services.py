"""Тесты сервисов."""
from datetime import datetime

import pytest

from src.cinema.models import Film, Viewer, Hall2D, Session, Cashier
from src.cinema.services import (
    SaleService, BookingService, TicketStorage, ReportService,
    NotificationService, EmailNotifier, SmsNotifier,
    FlatPrice, StudentDiscount, WeekendPrice, MorningDiscount,
)
from src.cinema.exceptions import AlreadySoldError, AgeLimitError, NotFoundError, BookingError


def make_session(age=12):
    return Session(
        Film("Дюна", "фантастика", 155, age),
        Hall2D("Зал 1", 5, 10),
        datetime(2026, 12, 1, 19, 30),
    )


def test_storage_add_get_remove():
    st = TicketStorage()
    item_id = st.add("билетик")
    assert st.get(item_id) == "билетик"
    assert item_id in st
    assert len(st) == 1
    st.remove(item_id)
    assert len(st) == 0


def test_storage_missing():
    st = TicketStorage()
    with pytest.raises(NotFoundError):
        st.get(999)


def test_sell_ok():
    ses = make_session()
    cashier = Cashier("Оля")
    sales = SaleService()
    t = sales.sell(ses, Viewer("Вася", "", 20), 1, cashier)
    assert t.cost == 300
    assert cashier.sales == 1
    assert sales.revenue() == 300


def test_sell_taken_fails():
    ses = make_session()
    sales = SaleService()
    v = Viewer("Вася", "", 20)
    sales.sell(ses, v, 1)
    with pytest.raises(AlreadySoldError):
        sales.sell(ses, v, 1)


def test_sell_age_fails():
    ses = make_session(age=18)
    sales = SaleService()
    with pytest.raises(AgeLimitError):
        sales.sell(ses, Viewer("Петя", "", 10), 1)


def test_book_and_buy_back():
    ses = make_session()
    v = Viewer("Вася", "", 20)
    booking = BookingService()
    sales = SaleService()
    booking.book(ses, v, 5)
    assert 5 not in ses.free_seats()
    t = booking.buy_booked(ses, 5, sales)
    assert t.seat == 5
    assert len(booking.bookings) == 0


def test_unbook_missing_fails():
    ses = make_session()
    with pytest.raises(BookingError):
        ses.unbook(3)


def test_notifiers_get_messages():
    ns = NotificationService()
    email = EmailNotifier()
    sms = SmsNotifier()
    ns.subscribe(email)
    ns.subscribe(sms)
    ns.notify_all("привет")
    assert email.sent == [("email", "привет")]
    assert sms.sent == [("sms", "привет")]
    ns.unsubscribe(sms)
    ns.notify_all("пока")
    assert len(sms.sent) == 1  # смс больше не приходят


def test_pricing():
    assert FlatPrice().calc(100) == 100
    assert StudentDiscount().calc(100) == 70
    # 28.11.2026 - суббота, 24.11.2026 - вторник
    assert WeekendPrice().calc(100, datetime(2026, 11, 28)) == 120
    assert WeekendPrice().calc(100, datetime(2026, 11, 24)) == 100
    assert MorningDiscount().calc(100, datetime(2026, 12, 1, 10, 0)) == 75
    assert MorningDiscount().calc(100, datetime(2026, 12, 1, 19, 0)) == 100


def test_report():
    ses = make_session()
    sales = SaleService()
    v = Viewer("Вася", "", 20)
    sales.sell(ses, v, 1)
    sales.sell(ses, v, 2)
    rep = ReportService(sales)
    assert rep.revenue_by_film() == {"Дюна": 600}
    assert rep.top_films(1) == [("Дюна", 2)]
    occ = rep.occupancy()
    assert occ[ses.id] == round(2 / 50 * 100, 1)
