class Commodity :
    def __init__(self, production_rate, min_threshold, trade_ratio, name, type, qty) :
        self.production_rate = production_rate
        self.min_threshold = min_threshold
        self.trade_ratio = trade_ratio
        self.name = name
        self.type = type
        self.qty = qty

    def be_consumed(self, amount) :
        self.qty -= amount

class TypeOne(Commodity) :
    # This type doesn't make anything and doesn't consume anything, eg. apples, wheat
    # (for now, apples obviously make apple pie)
    def __init__(self, production_rate, min_threshold, trade_ratio, name, qty) :
        super().__init__(production_rate, min_threshold, trade_ratio, name, "type_one", qty)

class TypeTwo(Commodity) :
    # This type makes things but doesn't consume anything, eg. trees
    def __init__(self, production_rate, min_threshold, trade_ratio, name, qty, product) :
        super().__init__(production_rate, min_threshold, trade_ratio, name, "type_two", qty)
        self.product = product

class TypeThree(Commodity) :
    # This type makes things and consumes things, eg. chickens eat wheat and apples and make eggs
    def __init__(self, production_rate, min_threshold, trade_ratio, name, qty, product, diet) :
        super().__init__(production_rate, min_threshold, trade_ratio, name, "type_three", qty)
        self.diet = diet
        self.product = product

class TypeFour(Commodity) :
    # this type is similar to type one, but gets consumed by the agents each cycle
    def __init__(self, production_rate, min_threshold, trade_ratio, name, qty, consume_quantity):
        super().__init__(production_rate, min_threshold, trade_ratio, name, "type_four", qty)
        self.consume_quantity = consume_quantity