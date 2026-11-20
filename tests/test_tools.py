from decimal import Decimal
import unittest

from tools.formatters import format_money
from tools.validators import parse_amount, parse_date


class ToolsTests(unittest.TestCase):
    def test_parse_amount_accepts_comma(self) -> None:
        self.assertEqual(parse_amount("1 250,50".replace(" ", "")), Decimal("1250.50"))

    def test_parse_amount_rejects_zero(self) -> None:
        with self.assertRaises(ValueError):
            parse_amount("0")

    def test_parse_date_rejects_wrong_format(self) -> None:
        with self.assertRaises(ValueError):
            parse_date("20.11.2026")

    def test_format_money(self) -> None:
        self.assertEqual(format_money(Decimal("1250.50")), "1 250,50 ₽")


if __name__ == "__main__":
    unittest.main()
