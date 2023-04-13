#! /usr/bin/env python3
import string
import calendar
from datetime import datetime


CALENDAR = [i for i in calendar.month_name[1:]]


def main():
    """
    Main Function of program.
    """
    # variables
    time = datetime.now()
    month = int(time.month) - 1
    index = 0

    # output months
    for i in CALENDAR:
        print(f"{i}: {index}")
        index += 1

    # verify input
    bad_chars = [i for i in string.ascii_letters] + [i for i in string.punctuation]

    birthday = input("Please input the index of your birth month.\n")

    if birthday in bad_chars:
        print("Cannot do numbers, sorry")
        exit()
    birthday = int(birthday)


    # output
    difference = month - birthday

    if difference == 0:
        print("Your birthday is this month.")

    elif difference < 0:
        print("Your birthday has not passed yet.")

    else:
        print("Your birthday has passed.")

if __name__ == "__main__":
    main()