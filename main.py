from inventory import Inventory
from totalInventory import total_inventory
from agent import agents, populate_agents, trade
from constants import TOTAL_DAYS
from logger import logger, clear_logs
        
# simulation data


def iterate_agents(day):
    total_inventory.clear_agent_statuses()
    for name, agent in agents.items():
        agent.react_to_markets(day)
        agent.consume_energy()
        agent.produce(day)
        agent.eat()
        agent.post_status()

def handle_agent_activities(day):
    logger(f"Today is day {day}")
    total_inventory.print_prices()
    iterate_agents(day)
    logger("\nQuantities Before Trading")
    view_agents()
    trade()
    total_inventory.adjust_prices(day)
    logger("\nQuantities After Trading")
    view_agents()
    logger("Total Inventories")
    total_inventory.view_total_inventories()

def iterate_time():
    for day in range(TOTAL_DAYS):
        handle_agent_activities(day)
        # agents do things

def view_agents():
    for name, agent in agents.items():
        agent.get_quantities()

    logger("\n")

def run_sim():
    clear_logs()
    populate_agents()
    total_inventory.populate_buckets()
    iterate_time()

run_sim()