from utils import prices, qty_to_make_products

class Commodity():
    def __init__(self, type, name, qty=0):
        self.qty = qty
        self.type = type
        self.name = name

    @property
    def trade_value(self):
        return prices[self.name]

    @property
    def qty_to_make_products(self):
        return qty_to_make_products[self.name]["total"]


class TypeOne(Commodity):  # edible
    def __init__(self, nutrition_value, name):
        super().__init__("type_one", name)
        self.nutrition_value = nutrition_value


class TypeTwo(Commodity):  # non-edible
    def __init__(self, name):
        super().__init__("type_two", name)


class TypeThree(Commodity): # replenishable and non-edible
    def __init__(self, name):
        super().__init__("type_three", name)


class Land(TypeThree):
    def __init__(self):
        super().__init__("land")
        self.harvest_day = 0
        self.qty_held = self.qty
        self.day_available = 0

    def update_qty_held(self, new_qty_held):
        self.qty_held = new_qty_held

    def get_qty_held(self):
        return self.qty_held

    def consume_resource(self, day, reuse_time, qty_consumed):
        self.day_available = day + reuse_time
        self.qty -= qty_consumed

    def make_available(self, day):
        if day >= self.day_available:
            self.qty = self.qty_held
            return True
        else:
            return False


class Wheat(TypeTwo):
    def __init__(self):
        super().__init__("wheat")
        self.production_values = {
            "land": {
                "qty_used": 16,
                "commodity_produced": 256,
                "reuse_time": 2
            }
        }


class Bread(TypeOne):
    def __init__(self):
        super().__init__(2, "bread")
        self.production_values = {
            "wheat": {
                "qty_used": 192,
                "commodity_produced": 24
            }
        }


class Strawberry(TypeOne):
    def __init__(self):
        super().__init__(4, "strawberry")
        self.production_values = {
            "land": {
                "qty_used": 16,
                "commodity_produced": 64,
                "reuse_time": 2
            }
        }

commodities = {
    "land": Land,
    "wheat": Wheat,
    "bread": Bread,
    "strawberry": Strawberry
}