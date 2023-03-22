#!/usr/bin/env python3

import random
from decorators import timed


def dice_game():
    """
    Runs the dice game.
    """
    # declare sides var so we can increase if needed in future
    sides = 6


    while True:
        # do the roll. sides + 1 since range is
        # inclusive beginning and exclusive end
        me = random.choice(range(1, sides + 1))
        player = random.choice(range(1, sides + 1))
        
        # declare bool values
        i_win = False
        tie = False

        # small if/elif tree to set vars as needed
        if me == player: tie = True
        elif me > player: i_win = True

        # nested ternary to get result
        result = "Tie" if tie else "I Win" if i_win else "You Win"


        # formatting output
        # print treats these strings as 1 connected string
        print(f"| Your Roll: {player} | "
              f"My Roll: {me} | "
              f"Result: {result} |"
              )
        
        # ask if we should play again and handle
        play_again = input("Play again?\n").lower()
        if "n" in play_again:
            break
        else:
            continue
    
# get performance characteristics
@timed
def main():
    """
    Main component of program.
    """
    dice_game()


if __name__ == "__main__":
    # get time of function
    null, ns, s = main()
    print(f"Function ran in {ns} nanoseconds | {s} seconds.")