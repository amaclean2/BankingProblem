from goodsList import goods_list, goods_map
from constants import INITIAL_QTY, PERISH_QTY, PRODUCTION_QTY, LOW_THRESHOLD, HIGH_THRESHOLD

class Agent:
    def __init__(self, production, name) :
        self.items = {}
        self.name = name
        self.production_item = production

    def set_initial_quantities(self) :
        for good in goods_list :
            self.items[good] = INITIAL_QTY if self.production_item == good else 0

    def perish_perishables(self) :
        # each chicken takes 2 apples and 5 wheats
        chickens = self.items["chickens"]
        for label, qty in self.items.items() :
            self.items[label] -= PERISH_QTY if label == "chickens" else goods_map[label]["consumable"] * chickens

    def produce(self) :
        if self.items[self.production_item] <= HIGH_THRESHOLD :
            self.items[self.production_item] += PRODUCTION_QTY * goods_map[self.production_item]["produce"]

    def get_lists(self) :
        lists = []
        for label, qty in self.items.items() :
            if qty < LOW_THRESHOLD * goods_map[label]["threshold"] :
                lists.append(f"low_{label}")
            elif qty > HIGH_THRESHOLD * goods_map[label]["threshold"] :
                lists.append(f"high_{label}")

        return lists

    def accept_item(self, item) :
        self.items[item] += 1

    def give_item(self, item) :
        self.items[item] -= 1