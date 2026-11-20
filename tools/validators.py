"""Проверка данных, вводимых пользователем."""

from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation


def parse_amount(value: str) -> Decimal:
    """Преобразует введённую сумму в положительное десятичное число."""
    try:
        amount = Decimal(value.replace(",", ".").strip())
    except InvalidOperation as error:
        raise ValueError("Введите сумму числом, например: 1250.50") from error

    if amount <= 0:
        raise ValueError("Сумма должна быть больше нуля.")
    return amount.quantize(Decimal("0.01"))


def parse_date(value: str) -> str:
    """Проверяет дату формата ГГГГ-ММ-ДД и возвращает её в том же формате."""
    try:
        return date.fromisoformat(value.strip()).isoformat()
    except ValueError as error:
        raise ValueError("Введите дату в формате ГГГГ-ММ-ДД, например: 2026-11-20") from error
