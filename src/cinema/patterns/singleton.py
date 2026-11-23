"""Синглтон через метакласс."""


class SingletonMeta(type):
    """Метакласс, не даёт создать больше одного объекта класса."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in SingletonMeta._instances:
            SingletonMeta._instances[cls] = super().__call__(*args, **kwargs)
        return SingletonMeta._instances[cls]


class CinemaRegistry(metaclass=SingletonMeta):
    """Общий реестр кинотеатров, он один на всю программу."""

    def __init__(self):
        self.cinemas = {}

    def register(self, name, cinema):
        """Запомнить кинотеатр по имени."""
        self.cinemas[name] = cinema

    def get(self, name):
        """Достать кинотеатр по имени, вернёт None если нет."""
        return self.cinemas.get(name)

    def all(self):
        """Все кинотеатры."""
        return dict(self.cinemas)
