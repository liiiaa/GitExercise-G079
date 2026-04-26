import random

flavors = ["Vanilla", "Chocolate", "Strawberry"]
toppings = ["Sprinkles", "Chocolate Chips", "Fruit"]

def generate_order():
    return {
        "flavor": random.choice(flavors),
        "toppings": random.sample(toppings, k=random.randint(1, 2))
    }