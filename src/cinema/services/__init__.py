"""Сервисы кинотеатра."""
from src.cinema.services.storage import TicketStorage
from src.cinema.services.pricing import (
    PriceStrategy,
    FlatPrice,
    StudentDiscount,
    WeekendPrice,
    MorningDiscount,
)
from src.cinema.services.sales import SaleService
from src.cinema.services.booking import BookingService
from src.cinema.services.notify import NotificationService, EmailNotifier, SmsNotifier
from src.cinema.services.report import ReportService
