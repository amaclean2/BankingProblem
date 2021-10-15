from inventory import Inventory
from constants import AGENT_COUNT
from commodities import prices, commodities, qty_to_make_products
from logger import logger
from utils import round_qties

SURPLUS_MULTIPLIER = 2
LOWER_PRICE_LIMIT = 0.0625

class TotalInventory(Inventory):
    def __init__(self):
        super().__init__()
        self.food_list = []
        self.shortages = []
        self.surpluses = []
        self.statuses =  {}

    def populate_buckets(self):
        for name, instance in commodities.items():
            self.buckets[name] = instance()
            if self.buckets[name].type == "type_one" \
                or self.buckets[name].type == "type_four":
                self.food_list.append(name)

    def update_total_inventories(self, qty, bucket):
        self.buckets[bucket].qty += qty
    
    def clear_agent_statuses(self):
        self.statuses = {}

    def update_agent_statuses(self, agent_name, commodity, status):
        if commodity in self.statuses:
            if status in self.statuses[commodity]:
                if not agent_name in self.statuses[commodity][status]:
                    self.statuses[commodity][status].append(agent_name)
            else:
                self.statuses[commodity][status] = [agent_name]
        else:
            self.statuses[commodity] = {}
            self.statuses[commodity][status] = [agent_name]

    def solve_for_meal(self):
        return super().solve_for_meal(self.food_list)

    def define_market_state(self):
        for name, item in self.buckets.items():
            qty_to_make = qty_to_make_products[name]["total"]

            if item.type == "type_one" or item.type == "type_four":
                # if the item.qty is less than the agent count
                # times the optimized amount of that food per day
                # then the commodity is in shortage

                meal_list = self.solve_for_meal()
                optimized_amount = meal_list[name]
                minimum_food_in_market  = AGENT_COUNT * optimized_amount
                logger(f"Minimum food in market: {name} {minimum_food_in_market}")

                # shortages
                if item.qty < minimum_food_in_market and name not in self.shortages:
                    self.shortages.append(name)

                elif item.qty >= minimum_food_in_market and name in self.shortages:
                    self.shortages.remove(name)

                # surpluses
                
                if item.qty > minimum_food_in_market * SURPLUS_MULTIPLIER and name not in self.surpluses:
                    self.surpluses.append(name)

                elif qty_to_make > 0 and item.qty > qty_to_make * AGENT_COUNT and name not in self.surpluses:
                    self.surpluses.append(name)
                
                elif item.qty <= minimum_food_in_market * SURPLUS_MULTIPLIER and name in self.surpluses:
                    self.surpluses.remove(name)
            elif item.type != "type_three":
                # shortages
                if item.qty <= qty_to_make and name not in self.shortages:
                    self.shortages.append(name)

                elif item.qty > qty_to_make and name in self.shortages:
                    self.shortages.remove(name)
                
                # surpluses
                if qty_to_make > 0 and item.qty > qty_to_make * AGENT_COUNT and name not in self.surpluses:
                    self.surpluses.append(name)

                elif name in self.surpluses and item.qty < qty_to_make * AGENT_COUNT:
                    self.surpluses.remove(name)

        return (self.shortages, self.surpluses)

    def adjust_prices(self, day):
        shortages, surplues = self.define_market_state()

        for item in shortages:
            prices[item] *= 2

            if prices[item] > 1:
                prices[item] = round(prices[item])

        for item in surplues:
            if prices[item] > LOWER_PRICE_LIMIT:
                prices[item] /= 2
                prices[item] = round_qties(prices[item], 4)

        self._meal_quantities = {}

    def view_total_inventories(self):
        for name, bucket in self.buckets.items():
            logger(f"{name} | {bucket.qty}")
        
        logger(f"shortages: {self.shortages}, surpluses: {self.surpluses}")

        logger("\n")

    def print_prices(self):
        logger("Prices:")
        for name, price in prices.items():
            logger(f"{name} | {price}")

        logger("\n")

total_inventory = TotalInventory()