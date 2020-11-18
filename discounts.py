from collections import OrderedDict


class Discount:
    limits = OrderedDict({
        1000: 3,
        5000: 5,
        7000: 7,
        10000: 10,
        50000: 15
    })

    def get_discount(self, price: float) -> float:
        for key, value in reversed(sorted(self.limits.items())):
            if price >= key:
                return value

        return 0
