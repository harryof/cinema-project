"""Абстракции проекта: что объекты должны уметь.

Классы ниже только ОБЪЯВЛЯЮТ методы, не реализуют их.
Реализуют уже модели и сервисы.
"""

from abc import ABC, abstractmethod


class Infoable(ABC):
    """Умеет коротко рассказать о себе строкой."""

    @abstractmethod
    def info(self) -> str:
        ...


class Describable(ABC):
    """Умеет отдать себя словарём (для базы и json)."""

    @abstractmethod
    def describe(self) -> dict:
        ...


class Sellable(ABC):
    """Можно продать."""

    @abstractmethod
    def price(self) -> float:
        ...

    @abstractmethod
    def sell(self) -> None:
        ...


class Bookable(ABC):
    """Можно забронировать и снять бронь."""

    @abstractmethod
    def book(self, seat: int) -> None:
        ...

    @abstractmethod
    def unbook(self, seat: int) -> None:
        ...


class Notifier(ABC):
    """Канал уведомлений (почта, смс...)."""

    @abstractmethod
    def send(self, msg: str) -> None:
        ...


class Storage(ABC):
    """Хранилище объектов."""

    @abstractmethod
    def add(self, item) -> None:
        ...

    @abstractmethod
    def get(self, item_id: int):
        ...

    @abstractmethod
    def remove(self, item_id: int) -> None:
        ...

    @abstractmethod
    def all(self) -> list:
        ...
