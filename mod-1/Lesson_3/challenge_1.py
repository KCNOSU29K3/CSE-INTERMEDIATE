#!/usr/bin/env python3

from decorators import timed

# named as to prevent collision with inbuilt sum function
def sum_func(initial_investment:int|float, years:int):
    """
    Calculates a return amount given an initial investment 
    and a time span in years.

    Assumes 5% interest.
    """

    # declare value
    accumulated = initial_investment
    
    # do math
    for _ in range(years):
        # add interest
        accumulated += (accumulated * 0.05)
    
    # return with rounding.
    return round(accumulated, 2)

# get performance characteristics
@timed
def main():
    # get data
    invest = float(input("How much do you want to invest?\n$"))
    time = int(input("How many years do you want to invest for?\n"))
    # compute
    returns = sum_func(invest, time)
    
    # inform user
    print(f"You will have ${returns:.2f} after investing an initial cost of ${invest:.2f} for {time} years.")


if __name__ == "__main__":
    null, ns, s = main()

    print(f"Function ran in {ns} nanoseconds | {s:.2f} seconds.")