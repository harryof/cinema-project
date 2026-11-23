"""Чтоб проект можно было поставить как пакет."""
from setuptools import setup, find_packages

setup(
    name="cinema_project",
    version="1.0",
    packages=find_packages(),
    description="Итоговый проект: кинотеатр",
    python_requires=">=3.10",
)
