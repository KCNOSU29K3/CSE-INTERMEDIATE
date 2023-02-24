"""
Challenge 1 module.
"""

def get_food(price:int|float) -> str:
    """
    Returns a string of the food chosen based on input price.
    """
    # simple match statement
    match price:
        case 999.99:
            return "You Bought a raw Potato."
        case 5|5.00:
            return "You Bought a cooked Potato"
        case 28900|28900.00:
            return 'You bought a Moldy Orange.'
        case _:
            return "Whatever you got, it ain't ours."

def main() -> None:
    """
    main program.
    """
    items_list = [
        "Potato (raw) | $999.99",
        "Potato (cooked) | $5.00",
        "Moldy Orange | $28900.00"
    ]

    for item in items_list: print(item)

    # get amount of money
    cost = float(input("what is the cost of your item\n").strip("$"))
    print(get_food(cost))

if __name__ == "__main__":
    try:
        main()
    except ValueError:
        print("Thats... not a number. what do you want me to do with this. go away")
        exit(-1)
    except:
        print("Yikes I did a woopsie. Goodbye.")
        exit(-1)
    exit(0)