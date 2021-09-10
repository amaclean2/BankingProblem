
from agent import Agent
from goodsList import goods_list
from constants import CYCLES, AGENT_COUNT, GOODS_COUNT, HOARD_QTY, HOARDER_FREQ
from trades import transact

agents = {}
lists = {}
trade_categories = [["low_wheat", "high_chickens"], ["low_chickens", "high_wheat"]]
trade_counter = 0

def build_lists() :
    for good in goods_list :
        lists[f"low_{good}"] = []
        lists[f"high_{good}"] = []


def build_sim() :
    for inc in range(AGENT_COUNT) :
        if inc % GOODS_COUNT == 0 :
            agents[inc] = Agent(goods_list[inc % GOODS_COUNT], inc)
        else :
            agents[inc] = Agent(goods_list[inc % GOODS_COUNT], inc)

        agents[inc].set_initial_quantities()

    build_lists()

def add_agent_to_list(name, list) :
    if not name in lists[list] :
        lists[list].append(name)

def recalibrate_agent(agent) :
    agent_lists = agent.get_lists()
    for agent_list in agent_lists :
        add_agent_to_list(agent.name, agent_list)

    for list_name, list in lists.items() :
        if agent.name in list and not list_name in agent_lists :
            list.remove(agent.name)

def handle_agents() :
    for name, agent in agents.items() :
        agent.perish_perishables()
        agent.produce()

        recalibrate_agent(agent)

'''
    an agent that doesn't have enough of something needs to trade with someone that has
    an abundance of that thing in exchange for something it needs that the first agent
    has an abundance of.

    i[0] is something the first agent needs
    i[1] is something the first agent has
    i is the comodity we are currently dealing with

    this method doesn't look for who needs what the current agent has an abundance of,
    but who has an abundance of what the current agent needs. It's more of a greedy algorithm
'''
def trade() :
    for good in goods_list :
        bail = False
        low_good = f"low_{good}"
        # assuming every good is going to have some agents that are low on it

        while len(lists[low_good]) > 0 and bail == False:
            # looping through all the agents that are low on that good
            # bail means there's no one to trade with and that agent has to be left alone
            agent = agents[lists[low_good][0]]

            # determine what that agent has an abundance of
            agent_lists = agent.get_lists()
            available_lambda = lambda str: str.find("high") != -1
            available_good = next(filter(available_lambda, agent_lists), None)
            # list to trade with is the agents that have an abundance of what you need
            list_to_trade_with = low_good.replace("low", "high")

            if len(lists[list_to_trade_with]) > 0 and available_good != None:
                trader = agents[lists[list_to_trade_with][0]]

                print(lists[low_good][0], trader.name, lists, low_good, available_good)

                giving_item = good
                taking_item = available_good.replace("high_", "")

                global trade_counter
                if trade_counter % HOARDER_FREQ == 0 :
                    for i in range(HOARD_QTY) :
                        transact(agent, trader, giving_item, taking_item)

                else :
                    transact(agent, trader, giving_item, taking_item)

                recalibrate_agent(agent)
                recalibrate_agent(trader)

                trade_counter += 1

            else :
                bail = True

def view_agents() :
    for name, agent in agents.items() :
        print(name, "|", agent.items["chickens"], "chickens,", agent.items["wheat"], "wheat", agent.items["apples"], "apples")

    print("low wheat", lists["low_wheat"])
    print("low chickens", lists["low_chickens"])
    print("high wheat", lists["high_wheat"])
    print("high chickens", lists["high_chickens"])
    print("high apples", lists["high_apples"])
    print("low apples", lists["low_apples"])
    print("\n")

def run_sim() :
    build_sim()
    for cycle in range(CYCLES) :
        handle_agents()
        trade()
        view_agents()