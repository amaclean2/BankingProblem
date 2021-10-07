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

my_list = []

for i in range(10):
    if i % 3 == 0:
        my_list.append("Happy Thirds!")

    elif i % 2 == 0:
        my_list.append("Evens Rule!")

    else:
        my_list.append("I'm Prime!")

print(my_list)