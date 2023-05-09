#! /usr/bin/env python3


def add_inventory(inventory, fruit, quantity:int=0):
    if inventory.get(fruit) is None:
        inventory[fruit] = quantity
        return 0
    inventory[fruit]=inventory[fruit] + quantity
    return 0


def main():
    inventory = {
        "apples":15,
        "bananas":35,
        "grapes":12
    }

    add_inventory(inventory, "strawberries", 10)

    assert inventory.get("strawberries") is not None
    assert inventory["strawberries"] == 10

    add_inventory(inventory, "strawberries", 25)

    assert inventory["strawberries"] == 35

    print(inventory)

if __name__ == "__main__":
    main()