from inventory import Inventory
from totalInventory import total_inventory
from constants import AGENT_COUNT
from commodities import prices, qty_to_make_products, get_commodity_to_start
from utils import add_qty_to_make_products, round_qties, cannot_be_made
from logger import logger
import math as m


class Agent(Inventory):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.energy = 128
        self.commodity_produced = get_commodity_to_start(self.name)
        self.task_energy = 8
        self.resources_out = []

    def build_resources_out(self):
        # the resources an agent is out of
        for name, bucket in self.buckets:
            if bucket.type != "type_three":
                self.resources_out.append(name)

    def consume_energy(self):
        self.energy -= self.task_energy
        logger(
            f"{self.name} has energy {self.energy}, and produces {self.commodity_produced}")

    def switch_commodity_produced(self, new_commodity):
        self.commodity_produced = new_commodity

    def grow_the_growables(self):
        for name, bucket in self.buckets.items():
            if bucket.type == "type_four":
                for rn, resource in bucket.production_values.items():
                    if self.buckets[rn].qty > resource["qty_used"]:
                        pr_rate = resource["commodity_produced"]
                        parents = self.buckets[rn].qty / resource["qty_used"]
                        parents -= parents % 1
                        total = pr_rate * parents
                        
                        bucket.qty += total
                        total_inventory.update_total_inventories(total, name)

    def produce(self, day):
        # take resources and turn them into product
        # in this case the resource is land and the product is wheat
        # an agent can grow so much wheat on some land but then the land is used up
        # the land is available again after 2 turns
        # also the agent consumes energy turning land into wheat
        commodity_produced = self.buckets[self.commodity_produced]
        resources = commodity_produced.production_values
        # resources refers to the varibles defining using the resource

        supplies = {}
        lowest_ratio = ["", 1]
        total_yield = 0

        self.grow_the_growables()

        for resource_name, resource in resources.items():
            inventory_resource = self.buckets[resource_name]

            # if the resource is ready today, make it available (primarily land)
            if inventory_resource.type == "type_three":
                is_available = inventory_resource.make_available(day)

                if is_available:
                    total_inventory.update_total_inventories(
                        inventory_resource.qty, resource_name)

            # supply accumulation
            if total_yield == 0:
                total_yield = resource["commodity_produced"]

            if inventory_resource.qty < resource["qty_used"]:
                working_ratio = inventory_resource.qty / resource["qty_used"]
                if working_ratio < lowest_ratio[1]:
                    lowest_ratio = [resource_name, working_ratio]

                supplies[resource_name] = inventory_resource.qty
                self.account_for_resources(resource_name)
            else:
                supplies[resource_name] = resource["qty_used"]

            add_qty_to_make_products(
                resource_name,
                self.commodity_produced,
                resource["qty_used"]
            )

        if self.energy > self.task_energy and len(supplies) > 0:
            if lowest_ratio[1] < 1:
                # deal with not enough resources
                for supply_name, supply_qty in supplies.items():
                    if supply_name != lowest_ratio[0]:
                        # rounding qty_used to the hundreds place cause this is getting ridiculous
                        qty_used = round_qties(supply_qty * lowest_ratio[1])
                        self.buckets[supply_name].qty -= qty_used
                        # update total inventory
                        total_inventory.update_total_inventories(
                            -1 * qty_used,
                            supply_name
                        )
                    else:
                        self.buckets[supply_name].qty = 0
                        # update total inventory
                        total_inventory.update_total_inventories(
                            -1 * supply_qty,
                            supply_name
                        )

                total_yield = round_qties(total_yield * lowest_ratio[1])
                commodity_produced.qty += total_yield

                if total_yield > 0:
                    self.consume_energy()
            else:
                # use up reseources
                for supply_name, supply_qty in supplies.items():
                    self.buckets[supply_name].qty -= supply_qty
                    # update total inventory
                    total_inventory.update_total_inventories(
                        -1 * supply_qty,
                        supply_name
                    )

                # make product s
                commodity_produced.qty += total_yield
                self.consume_energy()

            # udpate total_inventory
            total_inventory.update_total_inventories(total_yield, self.commodity_produced)

    def account_for_resources(self, resource):
        if self.buckets[resource].qty == 0:
            if not resource in self.resources_out:
                self.resources_out.append(resource)
        
        else:
            if resource in self.resources_out:
                self.resources_out.remove(resource)

    def react_to_markets(self, day):
        # if the agent is out of all supplies then they need to switch to 
        # making something from land
        if len(self.resources_out) >= len(self.buckets) - 1:
            self.switch_commodity_produced(get_commodity_to_start(self.name))
        else:
            # if the price of some commodity is greater than the one currently
            # being produced then switch to that one
            highest_price = "bread"
            for name, price in prices.items():
                if price > prices[highest_price] and self.buckets[name].type not in cannot_be_made:
                    highest_price = name

            if prices[self.commodity_produced] < prices[highest_price]:
                if day % AGENT_COUNT == self.name:
                    # this makes the agents switch what they produce more slowly
                    self.switch_commodity_produced(highest_price)

    def eat(self):
        quantities = total_inventory.solve_for_meal()
        added_energy = 0
        logger(f"Dinner: {quantities}")

        if len(quantities) > 0:
            # eat something
            for name, qty in quantities.items():
                bucket = self.buckets[name]

                if bucket.qty < qty:
                    added_energy += bucket.nutrition_value * bucket.qty

                    total_inventory.update_total_inventories(
                        -1 * bucket.qty,
                        name
                    )

                    bucket.qty = 0
                    self.account_for_resources(name)
                else:
                    added_energy += bucket.nutrition_value * qty

                    total_inventory.update_total_inventories(
                        -1 * qty,
                        name
                    )

                    bucket.qty -= qty

            self.energy += added_energy
        else:
            # you need food
            pass

    def get_quantities(self):
        for name, bucket in self.buckets.items():
            logger(f"{self.name} | {name}: {bucket.qty}")

    def get_statuses(self):
        take = {}
        give = {}

        optimized_ratios = total_inventory.solve_for_meal()
        for bucket_name, bucket in self.buckets.items():
            if bucket.type != "type_three":

                commodity_production_values = self.buckets[self.commodity_produced].production_values

                # if it's a resource and I don't have enough to make the next batch, take it
                # if it's food and I don't have enough for the next meal, take it

                # if it's food and I have an excess, get rid of it
                # anything else but land, get rid of it

                if bucket_name in commodity_production_values:
                    qty_used = commodity_production_values[bucket_name]["qty_used"]

                    if bucket.qty < qty_used:
                        qty_needed = qty_used - bucket.qty
                        take[bucket_name] = qty_needed
                    elif bucket_name in optimized_ratios and bucket.qty < optimized_ratios[bucket_name]:
                        qty_needed = optimized_ratios[bucket_name] - bucket.qty
                        take[bucket_name] = qty_needed

                elif bucket_name in optimized_ratios:
                    if bucket.qty < optimized_ratios[bucket_name]:
                        qty_needed = optimized_ratios[bucket_name] - bucket.qty
                        take[bucket_name] = qty_needed
                    elif bucket.qty >= optimized_ratios[bucket_name] * 2:
                        qty_to_give = bucket.qty - optimized_ratios[bucket_name]
                        give[bucket_name] = qty_to_give

                else:
                    if bucket.qty > 0:
                        give[bucket_name] = bucket.qty

        return (take, give)

    def post_status(self):
        agent_need, agent_has = self.get_statuses()
        for need in list(agent_need):
            # agent_need = {"bread": 5, "wheat": 3}
            total_inventory.update_agent_statuses(self.name, need, "need")

        for has in list(agent_has):
            total_inventory.update_agent_statuses(self.name, has, "has")


agents = {}

def populate_agents():
    for i in range(AGENT_COUNT):
        agents[i] = Agent(i)
        agents[i].populate_buckets()

        for name, bucket in agents[i].buckets.items():
            if bucket.type != "type_three":
                agents[i].resources_out.append(name)

def trade():
    logger("\nTrading")
    for commodity_name, commodity in total_inventory.statuses.items():

        if 'need' in commodity and 'has' in commodity and len(commodity['has']) > 0:

            while len(commodity["need"]) > 0 and len(commodity["has"]) > 0:
                agent_name = commodity["need"][0]
                # establish the two agents
                agent_one = agents[agent_name]
                logger(f"{commodity_name} has: {commodity}, name: {agent_name}")

                agent_two = agents[commodity['has'][0]]

                # establish quantites to trade
                take, give = agent_one.get_statuses()
                double_take, double_give = agent_two.get_statuses()
                # get_statuses() returns a dict

                if len(give) > 0:
                    # if agent_one has anything to give
                    take_price = agent_one.buckets[commodity_name].trade_value
                    give_price = agent_one.buckets[list(give)[0]].trade_value

                    # if agent_two has more than enough to give agent_one
                    if double_give[commodity_name] >= take[commodity_name]:
                        # how many does agent_one need/have to give?
                        take_qty = take[commodity_name]

                    else:
                        take_qty = double_give[commodity_name]

                    local_take_price = take_qty
                    local_give_price = (take_price * take_qty) / give_price

                    if local_give_price > agent_one.buckets[list(give)[0]].qty:
                        local_give_price = agent_one.buckets[list(give)[0]].qty
                        local_take_price = (local_give_price * give_price) / take_price


                    # trade the quantites
                    logger(f"{agent_one.name} | take: {commodity_name} {local_take_price}")

                    logger(f"{agent_two.name} | take: {list(give)[0]} {local_give_price}")

                    agent_one.buckets[commodity_name].qty += local_take_price
                    agent_one.buckets[list(give)[0]].qty -= local_give_price

                    agent_two.buckets[list(give)[0]].qty += local_give_price
                    agent_two.buckets[commodity_name].qty -= local_take_price

                    agent_one.account_for_resources(commodity_name)
                    agent_two.account_for_resources(list(give)[0])

                    # fix the statuses list
                    total_inventory.statuses[commodity_name]["need"].remove(agent_one.name)
                    total_inventory.statuses[list(give)[0]]["has"].remove(agent_one.name)

                    total_inventory.statuses[commodity_name]["has"].remove(agent_two.name)

                    try:
                        if agent_two.name in total_inventory.statuses[list(give)[0]]["need"]:
                            total_inventory.statuses[list(give)[0]]["need"].remove(agent_two.name)
                    except Exception as e:
                        logger(f"no {e} category in total_inventory.statuses[{list(give)[0]}]")

                    agent_one.post_status()
                    agent_two.post_status()

                    logger("-------")

                else:
                    total_inventory.statuses[commodity_name]["need"].remove(agent_one.name)

    logger("\n")
