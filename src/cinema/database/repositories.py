"""Репозитории: кладут модели в базу и достают обратно."""
from src.cinema.models import Film, Viewer, Session


class FilmRepository:
    """Фильмы в базе."""

    def __init__(self, db):
        self.db = db

    def save(self, film):
        """Сохранить фильм, вернёт его id в базе."""
        cur = self.db.execute(
            "INSERT INTO films (title, genre, duration, age_rating) VALUES (?, ?, ?, ?)",
            (film.title, film.genre, film.duration, film.age_rating),
        )
        return cur.lastrowid

    def get(self, film_id):
        """Достать фильм по id."""
        row = self.db.fetch_one("SELECT * FROM films WHERE id = ?", (film_id,))
        if row is None:
            return None
        return Film(row["title"], row["genre"], row["duration"], row["age_rating"])

    def all(self):
        """Все фильмы."""
        rows = self.db.fetch_all("SELECT * FROM films")
        return [Film(r["title"], r["genre"], r["duration"], r["age_rating"]) for r in rows]


class ViewerRepository:
    """Зрители в базе."""

    def __init__(self, db):
        self.db = db

    def save(self, viewer):
        """Сохранить зрителя, вернёт id."""
        cur = self.db.execute(
            "INSERT INTO viewers (name, email, age) VALUES (?, ?, ?)",
            (viewer.name, viewer.email, viewer.age),
        )
        return cur.lastrowid

    def get(self, viewer_id):
        """Достать зрителя по id."""
        row = self.db.fetch_one("SELECT * FROM viewers WHERE id = ?", (viewer_id,))
        if row is None:
            return None
        return Viewer(row["name"], row["email"], row["age"])

    def all(self):
        """Все зрители."""
        rows = self.db.fetch_all("SELECT * FROM viewers")
        return [Viewer(r["name"], r["email"], r["age"]) for r in rows]


class SessionRepository:
    """Сеансы в базе, переводит их в словари через to_dict."""

    SELECT = """
        SELECT s.id AS sid, f.title, f.genre, f.duration, f.age_rating,
               h.name, h.type, h.rows, h.seats_in_row, s.start
        FROM sessions s
        JOIN films f ON f.id = s.film_id
        JOIN halls h ON h.id = s.hall_id
    """

    def __init__(self, db):
        self.db = db

    def save(self, session):
        """Сохранить сеанс вместе с фильмом и залом."""
        d = session.to_dict()
        cur = self.db.execute(
            "INSERT INTO films (title, genre, duration, age_rating) VALUES (?, ?, ?, ?)",
            (d["film_title"], d["film_genre"], d["film_duration"], d["film_age"]),
        )
        film_id = cur.lastrowid
        cur = self.db.execute(
            "INSERT INTO halls (name, type, rows, seats_in_row) VALUES (?, ?, ?, ?)",
            (d["hall_name"], d["hall_type"], d["hall_rows"], d["hall_seats"]),
        )
        hall_id = cur.lastrowid
        cur = self.db.execute(
            "INSERT INTO sessions (film_id, hall_id, start) VALUES (?, ?, ?)",
            (film_id, hall_id, d["start"]),
        )
        session.id = cur.lastrowid  # id даёт база, чтоб не было совпадений
        return session.id

    def _row_to_session(self, row):
        """Строка из базы -> объект сеанса."""
        return Session.from_dict({
            "id": row["sid"],
            "film_title": row["title"],
            "film_genre": row["genre"],
            "film_duration": row["duration"],
            "film_age": row["age_rating"],
            "hall_name": row["name"],
            "hall_type": row["type"],
            "hall_rows": row["rows"],
            "hall_seats": row["seats_in_row"],
            "start": row["start"],
        })

    def get(self, session_id):
        """Достать сеанс по id."""
        row = self.db.fetch_one(self.SELECT + " WHERE s.id = ?", (session_id,))
        if row is None:
            return None
        return self._row_to_session(row)

    def all(self):
        """Все сеансы."""
        rows = self.db.fetch_all(self.SELECT)
        return [self._row_to_session(r) for r in rows]
