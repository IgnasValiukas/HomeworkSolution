import unittest
from main import apply_discount

class TestDiscountLogic(unittest.TestCase):
    def test_apply_discount_fully(self):
        total_discount = {}
        price, discount, updated_total = apply_discount(
            given_discount=2.0,
            given_price=5.0,
            remaining_discount=10.0,
            discount_month="2025-07",
            total_discount=total_discount
        )
        self.assertEqual(price, 3.0)
        self.assertEqual(discount, "2.00")
        self.assertEqual(updated_total, 2.0)

    def test_apply_discount_partially(self):
        total_discount = {"2025-07": 9.5}
        price, discount, updated_total = apply_discount(
            given_discount=2.0,
            given_price=6.9,
            remaining_discount=0.5,
            discount_month="2025-07",
            total_discount=total_discount
        )
        self.assertEqual(price, 6.4)
        self.assertEqual(discount, "0.50")
        self.assertEqual(updated_total, 10.0)

    def test_s_shipment_discount_applies(self):
        prices = {("S", "LP"): 1.5, ("S", "MR"): 2.0}
        size = "S"
        provider = "MR"
        price = prices[(size, provider)]
        min_price = min(p for (s, _), p in prices.items() if s == size)
        remaining = 10.0
        total_discount = {}
        month = "2025-07"
        initial_discount = price - min_price

        new_price, discount, updated_total = apply_discount(initial_discount, price, remaining, month, total_discount)

        self.assertEqual(new_price, 1.5)
        self.assertEqual(discount, "0.50")
        self.assertEqual(updated_total, 0.5)

    def test_third_l_lp_discount_applies(self):
        total_discount = {}
        remaining = 10.0
        price = 6.9
        month = "2025-07"
        new_price, discount, updated_total = apply_discount(price, price, remaining, month, total_discount)

        self.assertEqual(new_price, 0.0)
        self.assertEqual(discount, "6.90")
        self.assertEqual(updated_total, 6.9)

    def test_no_discount_needed_when_price_is_already_lowest(self):
        prices = {("S", "LP"): 1.5, ("S", "MR"): 2.0}
        size = "S"
        provider = "LP"
        price = prices[(size, provider)]
        min_price = min(p for (s, _), p in prices.items() if s == size)
        self.assertEqual(price, min_price)

    def test_discount_not_applied_when_budget_zero(self):
        total_discount = {"2025-07": 10.0}
        price, discount, updated_total = apply_discount(
            given_discount=2.0,
            given_price=5.0,
            remaining_discount=0.0,
            discount_month="2025-07",
            total_discount=total_discount
        )
        self.assertEqual(price, 5.0)
        self.assertEqual(discount, "0.00")
        self.assertEqual(updated_total, 10.0)

    def test_discount_cannot_exceed_remaining_budget(self):
        total_discount = {"2025-07": 9.0}
        price, discount, updated_total = apply_discount(
            given_discount=2.0,
            given_price=6.0,
            remaining_discount=1.0,
            discount_month="2025-07",
            total_discount=total_discount
        )
        self.assertEqual(price, 5.0)
        self.assertEqual(discount, "1.00")
        self.assertEqual(updated_total, 10.0)

if __name__ == "__main__":
    unittest.main()
