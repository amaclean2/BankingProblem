from goodsList import goods_list

# economy variables
CYCLES = 100
AGENT_COUNT = 6
GOODS_COUNT = len(goods_list)
HOARD_QTY = 1
HOARDER_FREQ = 5

# agent variables
INITIAL_QTY = 10
PERISH_QTY = 1
PRODUCTION_QTY = 4
LOW_THRESHOLD = 1
HIGH_THRESHOLD = 5

'''
    notes:
    production quantity really needs to be one above the amount of goods in the system
    agents should be a multiple of goods in the system for everyone to have someone to trade with
    to increase the thresholds the production quantities need to be increased
'''