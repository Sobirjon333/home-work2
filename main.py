"""Консольное приложение для личного учёта расходов."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

from tools.formatters import expenses_table, format_money
from tools.validators import parse_amount, parse_date

DATA_FILE = Path("expenses.json")


def load_expenses() -> list[dict[str, str]]:
    """Читает сохранённые расходы. При первом запуске создаёт пустой список."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open(encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Не удалось прочитать expenses.json. Начинаю с пустого списка.")
        return []
    return data if isinstance(data, list) else []


def save_expenses(expenses: list[dict[str, str]]) -> None:
    """Сохраняет список расходов в локальный JSON-файл."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, ensure_ascii=False, indent=2)


def add_expense(expenses: list[dict[str, str]]) -> None:
    """Запрашивает данные о новом расходе и добавляет его в список."""
    category = input("Категория: ").strip().title()
    description = input("Описание: ").strip()
    if not category or not description:
        print("Категория и описание не должны быть пустыми.")
        return

    try:
        amount = parse_amount(input("Сумма: "))
        entered_date = input(f"Дата [{date.today().isoformat()}]: ").strip()
        expense_date = parse_date(entered_date) if entered_date else date.today().isoformat()
    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    expenses.append(
        {
            "id": uuid4().hex[:8],
            "date": expense_date,
            "category": category,
            "description": description,
            "amount": str(amount),
        }
    )
    save_expenses(expenses)
    print("Расход сохранён.")


def show_summary(expenses: list[dict[str, str]]) -> None:
    """Показывает общую сумму и распределение расходов по категориям."""
    if not expenses:
        print("Расходов пока нет.")
        return

    totals: defaultdict[str, Decimal] = defaultdict(Decimal)
    for item in expenses:
        totals[item["category"]] += Decimal(item["amount"])

    total = sum(totals.values(), Decimal())
    print(f"\nВсего потрачено: {format_money(total)}")
    for category, amount in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"  • {category}: {format_money(amount)}")


def delete_expense(expenses: list[dict[str, str]]) -> None:
    """Удаляет расход по его идентификатору."""
    identifier = input("Введите ID расхода для удаления: ").strip()
    for index, item in enumerate(expenses):
        if item["id"] == identifier:
            removed = expenses.pop(index)
            save_expenses(expenses)
            print(f"Удалён расход: {removed['description']}.")
            return
    print("Расход с таким ID не найден.")


def main() -> None:
    """Запускает меню приложения."""
    expenses = load_expenses()
    actions = {
        "1": lambda: add_expense(expenses),
        "2": lambda: print("\n" + expenses_table(expenses)),
        "3": lambda: show_summary(expenses),
        "4": lambda: delete_expense(expenses),
    }

    while True:
        print("\n=== Учёт расходов ===\n1. Добавить расход\n2. Показать расходы\n3. Статистика\n4. Удалить расход\n0. Выход")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            print("До встречи!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Такого пункта нет. Попробуйте ещё раз.")


if __name__ == "__main__":
    main()
