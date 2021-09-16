from commodities.inventories import AgentInventory

class Agent(AgentInventory) :
    def __init__(self, commodity_produced, name) :
        super().__init__(commodity_produced)
        self.name = name

    def view_quantities(self) :
        commodity_quantities = f"{self.name} | "
        for commodity_name, quantity in self.get_bucket_quantities().items() :
            commodity_quantities += f"{commodity_name}: {quantity}, "

        return commodity_quantities[:-2]
