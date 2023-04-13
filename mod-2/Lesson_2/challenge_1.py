#! /usr/bin/env python3
import string

def main():
    """
    Main Function of program.
    """

    # variables
    cities = ["Edmonton", "Vancouver", "Cario", "Singapore", "Tokyo"]
    choice = input("Please choose a number from 0 to 4.\n")

    # character checking
    bad_chars = [i for i in string.ascii_letters] + [i for i in string.punctuation]
    if choice in bad_chars:
        print("Numbers only please.")
        exit()

    choice = int(choice)

    if choice > 4:
        choice = choice % 4

    # output
    print(f"{cities[choice]} is your suprise destination.")


if __name__ == "__main__":
    main()