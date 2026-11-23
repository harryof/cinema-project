"""Паттерны проектирования."""
from src.cinema.patterns.factory import SessionFactory
from src.cinema.patterns.singleton import SingletonMeta, CinemaRegistry
from src.cinema.patterns.decorator import (
    TicketDecorator,
    PopcornDecorator,
    ParkingDecorator,
    PremiumSeatDecorator,
)
from src.cinema.patterns.adapter import SessionAdapter
