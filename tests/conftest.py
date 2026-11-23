"""Общие фикстуры для тестов."""
import os
import sys
from datetime import datetime

import pytest

# чтоб тесты видели src и config из корня проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cinema.models import Film, Viewer, Hall2D, Session


@pytest.fixture
def film():
    return Film("Дюна", "фантастика", 155, 12)


@pytest.fixture
def hall():
    return Hall2D("Зал 1", 5, 10)


@pytest.fixture
def viewer():
    return Viewer("Вася", "vasya@mail.ru", 20)


@pytest.fixture
def session(film, hall):
    return Session(film, hall, datetime(2026, 12, 1, 19, 30))
