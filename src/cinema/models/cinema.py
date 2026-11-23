"""Сам кинотеатр: название, залы и сеансы."""
from config import CINEMA_NAME


class Cinema:
    """Кинотеатр, хранит залы и сеансы."""

    def __init__(self, name=CINEMA_NAME):
        self.name = name
        self.halls = []
        self.sessions = []

    def add_hall(self, hall):
        """Добавить зал."""
        self.halls.append(hall)

    def add_session(self, session):
        """Добавить сеанс."""
        self.sessions.append(session)

    def find_session(self, session_id):
        """Найти сеанс по id, вернёт None если нет."""
        for s in self.sessions:
            if s.id == session_id:
                return s
        return None

    def __len__(self):
        return len(self.halls)

    def __str__(self):
        return f"Кинотеатр «{self.name}», залов: {len(self.halls)}, сеансов: {len(self.sessions)}"
