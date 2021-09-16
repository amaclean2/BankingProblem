
from agent import Agent
from utils.constants import CYCLES, AGENT_COUNT, HOARD_QTY, HOARDER_FREQ
from commodities.inventories import GeneralInventory
from utils.logger import logger

agents = {}
trade_counter = 0

general_inventory = GeneralInventory()


def build_sim():
    goods_list = list(general_inventory.buckets)
    goods_count = len(goods_list)

    for inc in range(AGENT_COUNT):
        agents[inc] = Agent(goods_list[inc % goods_count], inc)


def handle_agents(cycle_no):
    for name, agent in agents.items():
        agent.consume(cycle_no)
        logger("agent finished consuming")
        agent.produce(cycle_no)
        general_inventory.update(agent)
        logger("agent finished producing")
        general_inventory.recalibrate_status_lists(agent)


def reduce_transaction_ratios(qty_1, qty_2):
    if (qty_1 < qty_2):
        temp = qty_1
        qty_1 = 1
        qty_2 = qty_2 / temp
    else:
        temp = qty_2
        qty_2 = 1
        qty_1 = qty_1 / temp

    return qty_1, qty_2

def transact(agent, trading_partner, item, trade_for_item):
    agent_receiving_quantity = general_inventory.buckets[item].trade_ratio
    agent_giving_quantity = general_inventory.buckets[trade_for_item].trade_ratio

    agent_receiving_quantity, agent_giving_quantity = \
        reduce_transaction_ratios(agent_receiving_quantity, agent_giving_quantity)

    logger(
        f"getting {agent_receiving_quantity} {item}, giving {agent_giving_quantity} {trade_for_item}")

    agent.accept_item(item, agent_receiving_quantity)
    agent.give_item(trade_for_item, agent_giving_quantity)

    trading_partner.accept_item(trade_for_item, agent_giving_quantity)
    trading_partner.give_item(item, agent_receiving_quantity)


'''
    an agent that doesn't have enough of something needs to trade with someone that has
    an abundance of that thing in exchange for something it needs that the first agent
    has an abundance of.

    i[0] is something the first agent needs
    i[1] is something the first agent has
    i is the comodity we are currently dealing with

    this method doesn't look for who needs what the current agent has an abundance of,
    but who has an abundance of what the current agent needs. It's more of a greedy algorithm

    the trade_ratio sets the amount of one item makes sense to trade for another
    since chickens consume so many consumables, it makes sense to set the trade ratio higher
    for chickens than another comodity
'''


def trade():
    for commodity_name in list(general_inventory.buckets):
        bail = False
        low_commodity = f"low_{commodity_name}"

        # assuming every good is going to have some agents that are low on it
        while len(general_inventory.statuses[low_commodity]) > 0 and bail == False:
            # looping through all the agents that are low on that good
            # bail means there's no one to trade with and that agent has to be left alone
            agent = agents[general_inventory.statuses[low_commodity][0]]

            # determine what that agent has an abundance of
            agent_lists = agent.get_statuses()
            def available_lambda(str): return str.find("high") != -1
            available_good = next(filter(available_lambda, agent_lists), None)
            # list to trade with is the agents that have an abundance of what you need
            agents_to_trade_with = low_commodity.replace("low", "high")
            logger(f"Trade Log\n---------")
            logger(f"getting agent: {agent.name}")
            logger(f"getting {low_commodity}, giving {available_good}")
            logger(f"general inventory statuses: {general_inventory.statuses}")

            if len(general_inventory.statuses[agents_to_trade_with]) > 0 and available_good != None:
                trading_partner = agents[general_inventory.statuses[agents_to_trade_with][0]]

                giving_item = available_good.replace("high_", "")
                taking_item = commodity_name
                logger(f"giving agent {trading_partner.name}")

                global trade_counter
                # if trade_counter % HOARDER_FREQ == 0 :
                #     for i in range(HOARD_QTY) :
                #         transact(agent, trading_partner, giving_item, taking_item)

                transact(agent, trading_partner, taking_item, giving_item)

                general_inventory.recalibrate_status_lists(agent)
                general_inventory.recalibrate_status_lists(trading_partner)

                trade_counter += 1

            else:
                bail = True


def view_statuses():
    print("Agent Statuses\n------------")
    for list_name, list in general_inventory.statuses.items():
        print(list_name, list)

    print("\n")


def view_agents():
    print("Agent Quantities\n------------")
    for name, agent in agents.items():
        print(agent.view_quantities())

    print("\n")


def view_general_inventory():
    print("Total Inventories\n------------")
    for name, bucket in general_inventory.buckets.items():
        commodity_per_agent = bucket.qty / AGENT_COUNT
        print(f"{name}: {bucket.qty}, per agent: {commodity_per_agent}")

    print("\n")


def run_sim():
    build_sim()
    for cycle in range(CYCLES):
        print(f"CYCLE {cycle}\n")
        general_inventory.reset()
        handle_agents(cycle)
        general_inventory.recalibrate_trade_ratios()
        trade()
        view_agents()
        view_statuses()
        view_general_inventory()

        print("================\n")
