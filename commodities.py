commodity_list = ["land", "wheat", "bread", "strawberry", "chicken", "egg"]

prices = { name: 1 for name in commodity_list }

qty_to_make_products = { name: { "total": 0 } for name in commodity_list }

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


class TypeFour(Commodity): # doesn't comsume it's resources
    def __init__(self, nutrition_value, name):
        super().__init__("type_four", name)
        self.nutrition_value = nutrition_value


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
                "commodity_produced": 128,
                "reuse_time": 2
            }
        }


class Bread(TypeOne):
    def __init__(self):
        super().__init__(2, "bread")
        self.production_values = {
            "wheat": {
                "qty_used": 192,
                "commodity_produced": 12 # one loaf
            }
        }


class Strawberry(TypeOne):
    def __init__(self):
        super().__init__(4, "strawberry")
        self.production_values = {
            "land": {
                "qty_used": 16,
                "commodity_produced": 32,
                "reuse_time": 2
            }
        }

class Chicken(TypeOne):
    def __init__(self):
        super().__init__(16, "chicken")
        self.production_values = {
            "land": {
                "qty_used": 8,
                "commodity_produced": 4,
                "reuse_time": 4
            },
            "wheat": {
                "qty_used": 64,
                "commodity_produced": 4 # one chicken
            }
        }

class Egg(TypeFour):
    def __init__(self):
        super().__init__(8, "egg")
        self.production_values = {
            "chicken": {
                "qty_used": 4,
                "commodity_produced": 1
            }
        }

commodities = {
    "land": Land,
    "wheat": Wheat,
    "bread": Bread,
    "strawberry": Strawberry,
    "chicken": Chicken,
    "egg": Egg
}

commodities_to_start = []

def get_commodity_to_start(agent_name):
    if len(commodities_to_start) > 0:
        return commodities_to_start[agent_name % len(commodities_to_start)]

    for name, instance in commodities.items():
        new_instance = instance()
        available_to_add = True

        if new_instance.type != "type_three":
            for pv_name in list(new_instance.production_values):
                if pv_name != "land":
                    available_to_add = False
        else:
            available_to_add = False

        if available_to_add:
            commodities_to_start.append(name)
    
    return commodities_to_start[agent_name % len(commodities_to_start)]