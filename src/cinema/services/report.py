"""Отчёты по продажам."""
from collections import Counter


class ReportService:
    """Считает статистику по проданным билетам."""

    def __init__(self, sale_service):
        self.sales = sale_service

    def revenue_by_film(self):
        """Выручка по каждому фильму."""
        result = {}
        for t in self.sales.tickets:
            name = t.session.film.title
            result[name] = result.get(name, 0) + t.cost
        return result

    def occupancy(self):
        """Заполняемость сеансов в процентах."""
        result = {}
        for t in self.sales.tickets:
            s = t.session
            result[s.id] = round(len(s.sold) / s.hall.capacity() * 100, 1)
        return result

    def top_films(self, n=3):
        """Самые продаваемые фильмы."""
        cnt = Counter(t.session.film.title for t in self.sales.tickets)
        return cnt.most_common(n)
