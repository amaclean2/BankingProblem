from sympy import symbols, Eq, solve
from math import ceil

from commodities import commodities
from logger import logger

# agent data


class Inventory():
    def __init__(self):
        self.buckets = {}
        self.foods = []
        self._meal_quantities = {}
        self.meal_value = 32

    def populate_buckets(self):
        for name, instance in commodities.items():
            self.buckets[name] = instance()

        self.buckets["land"].update_qty_held(16)

    def _set_up_variables_for_optimization(self, lowest_price, food_list):
        variables = ''

        # creating a string of variables to use in our optimization function
        for item in food_list:
            variables += f"{item},"
            if self.buckets[item].trade_value < self.buckets[lowest_price].trade_value:
                lowest_price = item

        # remove the last comma
        variables = variables[:-1]
        quantities = symbols(variables)
        return quantities, lowest_price

    def _build_equations(self, lowest_price, food_list, quantities):
        nutrition_eq = 0
        eqs = []

        for index, item in enumerate(food_list):
            price = self.buckets[item].trade_value / \
                self.buckets[lowest_price].trade_value

            if len(food_list) == 1:
                eqs.append(Eq((quantities), quantities))
                nutrition_eq += self.buckets[item].nutrition_value * quantities
            else:
                eqs.append(
                    Eq((price * quantities[index]),
                        quantities[food_list.index(lowest_price)])
                )
                nutrition_eq += self.buckets[item].nutrition_value * \
                    quantities[index]

        eqs.insert(0, Eq((nutrition_eq), self.meal_value))

        return nutrition_eq, eqs

    def get_meal_sums(self):
        # generator expression, list comprehension
        return sum(qty for name, qty in self._meal_quantities.items())

    def solve_for_meal(self, food_list):
        # if we already have our meal quantities, we don't need to recalculate it
        if len(self._meal_quantities) > 0:
            return self._meal_quantities

        logger("SOLVING FOR MEAL")
        if len(food_list) > 0:
            # lowest price is the name of the item with the lowest price
            lowest_price = food_list[0]
            quantities, lowest_price = self._set_up_variables_for_optimization(
                lowest_price,
                food_list
            )

            nutrition_eq, eqs = self._build_equations(
                lowest_price,
                food_list,
                quantities
            )

            if len(food_list) == 1:
                # if the length of quantities is 1 then 'solve' returns an array otherwise it returns a dict
                # we want to convert both of them to dicts
                quan_dict = {}
                quantities = solve((eqs[0]), quantities)
                quan_dict[food_list[0]] = ceil(quantities[0])

                quantities = quan_dict
            else:
                quantities = solve((eqs[0], *eqs[1:]), quantities)
                new_quantities = {}

                for key, value in quantities.items():
                    new_key = str(key)
                    new_quantities[new_key] = ceil(value)

                quantities = new_quantities

            self._meal_quantities = quantities

            logger(f"Meal totals: {self.get_meal_sums()}")

        else:
            self._meal_quantities = {}

        return self._meal_quantities
