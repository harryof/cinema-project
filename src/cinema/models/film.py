"""Фильм, который крутят в кинотеатре."""
from dataclasses import dataclass


@dataclass
class Film:
    """Фильм: название, жанр, сколько идёт и возрастной рейтинг."""

    title: str
    genre: str
    duration: int
    age_rating: int

    def __str__(self):
        return f"{self.title} ({self.age_rating}+)"
