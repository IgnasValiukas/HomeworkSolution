"""
Task:
1. All S shipments should always match the lowest S package price among the providers.
2. The third L shipment via LP should be free, but only once a calendar month.
3. Accumulated discounts cannot exceed 10 € in a calendar month.
If there are not enough funds to fully cover a discount this calendar month, it should be covered partially.

Design Decisions & Assumptions:
- Monthly logic is based on 'YYYY-MM' string parsing.
- Only LP and MR providers are valid.
- Discounts are capped at 10€ per calendar month.
- No external libraries are used (except for testing).

To run: python main.py
To test: python unit_test.py
"""

"""
Applies a discount to the shipment, up to the remaining budget for the month.
Updates total_discount and returns the new price, formatted discount, and updated total.
"""


def apply_discount(given_discount, given_price, remaining_discount, discount_month, total_discount):
    # checks if there's enough remaining discount budget
    actual_discount = min(given_discount, remaining_discount)
    given_price -= actual_discount
    calculated_discount = f"{actual_discount:.2f}"
    # tracks how much of the monthly limit has already been used
    total_discount[discount_month] = total_discount.get(discount_month, 0) + actual_discount
    return given_price, calculated_discount, total_discount[discount_month]


def main():
    # data is loaded from "input.txt"
    with open("input.txt", 'r') as file:
        lines = [line.strip() for line in file]

    # price dictionary with each size and provider
    prices = {
        ("S", "LP"): 1.5,
        ("M", "LP"): 4.9,
        ("L", "LP"): 6.9,
        ("S", "MR"): 2,
        ("M", "MR"): 3,
        ("L", "MR"): 4
    }

    l_lp_counter = {}
    total_discount = {}
    MAX_MONTHLY_DISCOUNT = 10

    for line in lines:
        # if data is valid it splits to 3 categories
        if len(line.split()) == 3:
            date, size, provider = line.split()
            if size in ["S", "M", "L"] and provider in ["LP", "MR"]:
                # extracts year and month as a substring for simplicity
                # for more flexible date handling can be used datetime library
                month = date[:7]
                # from prices dict. takes price that matches size and provider
                price = prices.get((size, provider), 0)
                discount = "-"
                # recalculates the remaining discount budget for the current month
                remaining = MAX_MONTHLY_DISCOUNT - total_discount.get(month, 0)

                # finds lowest S-sized price and applies discount
                if size == "S":
                    min_price = min(
                        price for (shipment_size, provider), price in prices.items() if shipment_size == size)
                    if remaining > 0 and price > min_price:
                        initial_discount = price - min_price
                        price, discount, total_discount[month] = apply_discount(initial_discount, price, remaining,
                                                                                month, total_discount)

                # applies a discount to every third L-size shipment per month
                elif provider == "LP" and size == "L":
                    # tracks how many L-sized packages in each month
                    l_lp_counter[month] = l_lp_counter.get(month, 0) + 1
                    if l_lp_counter[month] == 3:
                        initial_discount = price
                        price, discount, total_discount[month] = apply_discount(initial_discount, price, remaining,
                                                                                month, total_discount)

                print(f"{line} {price:.2f} {discount}")
            else:
                print(f'{line} Ignored')
        else:
            print(f'{line} Ignored')


if __name__ == "__main__":
    main()
