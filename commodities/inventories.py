from utils.logger import logger
from utils.constants import HIGH_TO_LOW_RATIO
from commodities.commodity import Chickens, Apples, Wheat, Eggs


class Inventory:
    def __init__(self):
        self.buckets = {
            "chickens": Chickens(),
            "apples": Apples(),
            "wheat": Wheat(),
            "eggs": Eggs()
        }

    def get_statuses(self):
        statuses = []
        for name, commodity in self.buckets.items():
            if commodity.qty < commodity.min_threshold:
                statuses.append(f"low_{name}")
            elif commodity.qty > commodity.min_threshold * HIGH_TO_LOW_RATIO:
                statuses.append(f"high_{name}")

        return statuses

    def get_bucket_quantities(self):
        qty_bucket = {}
        for name, commodity in self.buckets.items():
            qty_bucket[name] = commodity.qty

        return qty_bucket


class AgentInventory(Inventory):
    def __init__(self, commodity_produced="apples"):
        super().__init__()

        self.commodity_produced = commodity_produced
        self.buckets[commodity_produced].qty = self.buckets[commodity_produced].min_threshold * 2

    def set_commodity_produced(self, commodity_produced):
        self.commodity_produced = commodity_produced

    def consume(self, cycle_number):
        logger(f"bucket before consuming: {self.get_bucket_quantities()}")
        
        total_diet = {}
        for name, commodity in self.buckets.items():
            if commodity.type == "type_three":
                for item, qty in commodity.diet.items():
                    if item in total_diet:
                        total_diet[item] += qty * commodity.qty
                    else:
                        total_diet[item] = qty * commodity.qty
            if commodity.type == "type_four":
                commodity.qty -= commodity.consume_quantity

        for name, qty in total_diet.items():
            self.buckets[name].be_consumed(qty)

        logger(f"bucket after consuming: {self.get_bucket_quantities()}")

    def produce(self, cycle_number):
        logger(f"bucket before producing: {self.get_bucket_quantities()}")

        for name, commodity in self.buckets.items():
            if commodity.type == "type_two" or commodity.type == "type_three":
                for product_name, product_qty in commodity.product.items():
                    self.buckets[product_name].qty += product_qty * \
                        commodity.qty

        production_rate = self.buckets[self.commodity_produced].production_rate
        if production_rate < 1:
            if cycle_number % (1 / production_rate) == 0:
                self.buckets[self.commodity_produced].qty += 1

        else:
            self.buckets[self.commodity_produced].qty += production_rate

        logger(f"bucket after producing: {self.get_bucket_quantities()}")

    def accept_item(self, name, qty=1):
        logger(f"bucket before getting: {self.get_bucket_quantities()}")

        self.buckets[name].qty += qty

        logger(f"bucket after getting: {self.get_bucket_quantities()}")

    def give_item(self, name, qty=1):
        logger(f"bucket before giving: {self.get_bucket_quantities()}")

        self.buckets[name].qty -= qty

        logger(f"bucket after giving: {self.get_bucket_quantities()}")


class GeneralInventory(Inventory):
    def __init__(self):
        super().__init__()

        self.statuses = {}
        for name in list(self.buckets):
            self.statuses[f"low_{name}"] = []
            self.statuses[f"high_{name}"] = []

    def put_agent_in_status_list(self, name, status):
        if not name in self.statuses[status]:
            self.statuses[status].append(name)

    def recalibrate_status_lists(self, agent):
        agent_statuses = agent.get_statuses()

        for status in agent_statuses:
            self.put_agent_in_status_list(agent.name, status)

        for status_list_name, status_list in self.statuses.items():
            if agent.name in status_list and not status_list_name in agent_statuses:
                status_list.remove(agent.name)

    def reset(self):
        for name, bucket in self.buckets.items():
            bucket.qty = 0

    def update(self, agent):
        for name, bucket in agent.buckets.items():
            self.buckets[name].qty += bucket.qty

    def recalibrate_trade_ratios(self):
        for name, bucket in self.buckets.items():

            logger(f"{name} before tr adjust: {bucket.trade_ratio}")
            
            max_threshold = bucket.min_threshold * HIGH_TO_LOW_RATIO
            if bucket.qty > max_threshold * 2:
                bucket.trade_ratio *= 2
            elif bucket.qty < bucket.min_threshold:
                bucket.trade_ratio /= 2

            logger(f"{name} after tr adjust: {bucket.trade_ratio}")
