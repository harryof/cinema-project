"""Хранилище билетов в памяти."""
from src.cinema.interfaces import Storage
from src.cinema.exceptions import NotFoundError


class TicketStorage(Storage):
    """Хранит билеты в словаре, ключ - номер билета."""

    def __init__(self):
        self.data = {}
        self.next_id = 1

    def add(self, item):
        """Положить билет, вернёт его номер."""
        item_id = self.next_id
        self.next_id += 1
        self.data[item_id] = item
        return item_id

    def get(self, item_id):
        """Достать билет по номеру."""
        if item_id not in self.data:
            raise NotFoundError(f"нет билета с id {item_id}")
        return self.data[item_id]

    def remove(self, item_id):
        """Удалить билет."""
        if item_id not in self.data:
            raise NotFoundError(f"нет билета с id {item_id}")
        del self.data[item_id]

    def all(self):
        """Все билеты списком."""
        return list(self.data.values())

    def __len__(self):
        return len(self.data)

    def __contains__(self, item_id):
        return item_id in self.data

    def __getitem__(self, item_id):
        return self.get(item_id)

    def __iter__(self):
        return iter(self.data.values())
