from __future__ import annotations

from decimal import Decimal
from typing import Iterable, Mapping


def format_money(amount: Decimal) -> str:
    return f"{amount:,.2f}".replace(",", " ").replace(".", ",") + " ₽"


def expenses_table(expenses: Iterable[Mapping[str, str]]) -> str:
    rows = list(expenses)
    if not rows:
        return "Расходов пока нет."

    header = ("ID", "Дата", "Категория", "Описание", "Сумма")
    data = [
        (item["id"], item["date"], item["category"], item["description"], item["amount"])
        for item in rows
    ]
    widths = [max(len(row[index]) for row in [header, *data]) for index in range(len(header))]

    def line(row: tuple[str, ...]) -> str:
        return " | ".join(value.ljust(widths[index]) for index, value in enumerate(row))

    separator = "-+-".join("-" * width for width in widths)
    return "\n".join([line(header), separator, *(line(row) for row in data)])
