apples = {
    "apples": 3,
    "bananas": 5
}

class Fruit():
    def __init__(self, name, type):
        self.name = name
        self.type = type

    @property
    def trade_value(self):
        return apples[self.name]

class TypeOne(Fruit):
    def __init__(self, name):
        super().__init__(name, "type_one")

class Apples(TypeOne):
    def __init__(self):
        super().__init__("apples")
    

class Bananas(TypeOne):
    def __init__(self):
        super().__init__("bananas")


msg = "Hello World"
print(msg)

# my_list = []

# for i in range(10):
#     if i % 3 == 0:
#         my_list.append("Happy Thirds!")

#     elif i % 2 == 0:
#         my_list.append("Evens Rule!")

#     else:
#         my_list.append("I'm Prime!")

# print(my_list)

new_list = ["apples", "bananas", "carrots", "oranges", "watermelons", "cantaloupes"]
new_dict = {"apples": 3, "bananas": 2, "carrots": 10, "oranges": 5, "watermelons": 8, "cantaloupes": 7}

# sorted_data = sorted(new_list, key=lambda x: new_dict[x])

# print(sorted_data)

other_list = [3, 2, 10, 5, 8, 7]