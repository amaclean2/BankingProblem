from sympy import symbols, Eq, solve
from math import ceil

from commodities import commodities
from logger import logger

# agent data
class Inventory():
    def __init__(self):
        self.buckets = {}
        self.foods = []
        self.meal_quantities = {}
        self.meal_value = 16

    def populate_buckets(self):
        for name, instance in commodities.items():
            self.buckets[name] = instance()

        self.buckets["land"].update_qty_held(16)

    def solve_for_meal(self, food_list):
        if len(self.meal_quantities) > 0:
            return self.meal_quantities

        food_list_length = len(food_list)
        logger("SOLVING FOR MEAL")
        if len(food_list) > 0:
            # lowest price is the name of the item with the lowest price
            lowest_price = food_list[0]
            variables = ''

            for item in food_list:
                variables += f"{item},"
                if self.buckets[item].trade_value < self.buckets[lowest_price].trade_value:
                    lowest_price = item

            variables = variables[:-1]
            quantities = symbols(variables)
            nutrition_eq = 0
            eqs = []

            for index, item in enumerate(food_list):
                price = self.buckets[item].trade_value / \
                    self.buckets[lowest_price].trade_value

                if food_list_length == 1:
                    eqs.append(Eq((quantities), quantities))
                    nutrition_eq += self.buckets[item].nutrition_value * quantities
                else:
                    eqs.append(
                        Eq((price * quantities[index]), quantities[food_list.index(lowest_price)])
                    )
                    nutrition_eq += self.buckets[item].nutrition_value * \
                        quantities[index]

            eq1 = Eq((nutrition_eq), self.meal_value)

            if food_list_length == 1:
                # if the length of quantities is 1 then solve returns an array otherwise it returns a dict
                # we want to convert both of them to dicts
                quan_dict = {}
                quantities = solve((eq1), quantities)
                quan_dict[food_list[0]] = ceil(quantities[0])

                quantities = quan_dict
            else:
                quantities = solve((eq1, *eqs), quantities)
                new_quantities = {}

                for key, value in quantities.items():
                    new_key = str(key)
                    new_quantities[new_key] = ceil(value)

                quantities = new_quantities

            self.meal_quantities = quantities

        else:
            self.meal_quantities = {}

        return self.meal_quantities