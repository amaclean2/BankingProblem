from commodities.templates import TypeOne, TypeThree, TypeFour


class Apples(TypeFour):
    def __init__(self, qty=0):
        # production_rate, min_threshold, trade_ratio, name, qty, consume_quantity
        super().__init__(32, 4, 16, "apples", qty, 1)


class Wheat(TypeOne):
    def __init__(self, qty=0):
        # production_rate, min_threshold, trade_ratio, name, qty
        super().__init__(64, 1, 32, "wheat", qty)


class Eggs(TypeFour):
    def __init__(self, qty=0):
        # production_rate, min_threshold, trade_ratio, name, qty, consume_quantity
        super().__init__(2, 4, 16, "eggs", qty, 2)


class Chickens(TypeThree):
    def __init__(self, qty=0):
        # production_rate, min_threshold, trade_ratio, name, qty, product, diet
        super().__init__(0.5, 0, 1, "chickens", qty,
                         {"eggs": 2}, {"apples": 1, "wheat": 2})
