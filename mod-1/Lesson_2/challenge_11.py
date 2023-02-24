#! usr/bin/env python3

import random
import string

get_discount_amount  = lambda : random.choice([10, 20, 30])

def calc(prices:list[int|float], discount_percentage:int):
    """
    Calculates the total cost of the purchase, minus a discount percent and including GST.
    
    ### Parameters

    `purchase` A list containing the prices for all items in the purchase.

    `discount_percent` The percent to remove off of the purchase.

    ### Returns

    `int` the full price.
    """

    x = sum(prices)
    # apply discount
    x = x - (x*(discount_percentage/100))
    # apply gst
    return (round(x + (x*0.05), 2))


def main():

    # declare needed variables
    items_list = []
    cost_list = []
    # declare a filter list
    filter_list = [i for i in string.ascii_letters + string.punctuation]
    filter_list.remove(".")

    print('Please enter the prices of your items here.')

    # event loop
    for i in range(3):
            
        try:

            # get and format item
            new_item = input(" ")
            items_list.append(new_item)
            new_item = new_item.replace(",", ".")
            for letter in filter_list:
                new_item = new_item.replace(letter, "")
            
            num_list = [i for i in string.digits]

            # handling inputs w/o numbers
            # here we fail open since the user put in the item w/o a price
            detected = False
            for i in num_list:
                if i in new_item:
                    detected = True
            
            if not detected: continue

            # handling decimals in front of cost + spaces
            # slice a bit off
            while new_item[0:1] not in num_list:
                new_item = new_item[1:]

            # append item
            cost_list.append(float(new_item))
        
        # catch failure
        except ValueError:
            print("Invalid item entered.")
            print("Press Enter to continue")
            input()
            continue
    
    cost = calc(cost_list, get_discount_amount())
    print('Your cost is ${:.2f}'.format(cost))

if __name__ == "__main__":
    main()