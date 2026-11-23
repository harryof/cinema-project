"""Тесты базы данных."""
from datetime import datetime

from src.cinema.models import Film, Viewer
from src.cinema.database import (
    DatabaseManager, FilmRepository, ViewerRepository, SessionRepository,
)
from src.cinema.patterns import SessionFactory


def test_film_roundtrip(tmp_path):
    db_path = str(tmp_path / "test.db")
    with DatabaseManager(db_path) as db:
        db.init_db()
        repo = FilmRepository(db)
        fid = repo.save(Film("Дюна", "фантастика", 155, 12))
        got = repo.get(fid)
        assert got.title == "Дюна"
        assert got.age_rating == 12
        assert len(repo.all()) == 1


def test_viewer_roundtrip(tmp_path):
    db_path = str(tmp_path / "test.db")
    with DatabaseManager(db_path) as db:
        db.init_db()
        repo = ViewerRepository(db)
        vid = repo.save(Viewer("Вася", "vasya@mail.ru", 20))
        got = repo.get(vid)
        assert got.name == "Вася"
        assert got.email == "vasya@mail.ru"


def test_session_roundtrip(tmp_path):
    db_path = str(tmp_path / "test.db")
    ses = SessionFactory.make_session(
        "imax", "Аймакс", 5, 10, "Дюна", "фантастика", 155, 12,
        datetime(2026, 12, 1, 19, 30),
    )
    with DatabaseManager(db_path) as db:
        db.init_db()
        repo = SessionRepository(db)
        sid = repo.save(ses)
        got = repo.get(sid)
        assert got.film.title == "Дюна"
        assert got.hall.base_price() == 650
        assert got.start == datetime(2026, 12, 1, 19, 30)
        assert len(repo.all()) == 1


def test_get_missing(tmp_path):
    db_path = str(tmp_path / "test.db")
    with DatabaseManager(db_path) as db:
        db.init_db()
        assert FilmRepository(db).get(123) is None
        assert SessionRepository(db).get(123) is None
