import random

orders = [
    "Vanilla Ice Cream",
    "Chocolate Milkshake",
    "Strawberry Ice Cream",
    "Choco Mint Ice Cream"
]

def generate_order():
    return random.choice(orders)