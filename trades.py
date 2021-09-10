def build_trade_categories() :
    pass

def transact(agent, trader, item, trade_for_item) :
    agent.accept_item(item)
    agent.give_item(trade_for_item)

    trader.accept_item(trade_for_item)
    trader.give_item(item)