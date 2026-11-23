"""Уведомления, тут паттерн наблюдатель."""
from src.cinema.interfaces import Notifier


class EmailNotifier(Notifier):
    """Шлёт на почту (ну типа шлёт)."""

    def __init__(self):
        self.sent = []

    def send(self, msg):
        self.sent.append(("email", msg))
        print(f"[EMAIL] {msg}")


class SmsNotifier(Notifier):
    """Шлёт смс."""

    def __init__(self):
        self.sent = []

    def send(self, msg):
        self.sent.append(("sms", msg))
        print(f"[SMS] {msg}")


class NotificationService:
    """Разсылает сообщение всем, кто подписался."""

    def __init__(self):
        self.subs = []

    def subscribe(self, notifier):
        """Подписать на уведомления."""
        self.subs.append(notifier)

    def unsubscribe(self, notifier):
        """Отписать."""
        self.subs.remove(notifier)

    def notify_all(self, msg):
        """Отправить всем подписчикам."""
        for n in self.subs:
            n.send(msg)
