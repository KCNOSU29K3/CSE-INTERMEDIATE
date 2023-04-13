#! /usr/bin/env python3
import string


def find_highest(marks:list[int]):
    """
    Returns highest value of list
    """
    marks.sort(reverse=True)
    return marks[0]


def main():
    """
    Main Function of program.
    """
    marks = []
    good_chars = [i for i in string.digits]
    good_chars.append(".")

    print("Please enter a set of marks.")

    for i in range(5):
        mark = input()

        for char in mark:
            if char not in good_chars:
                print("bad input.")
                exit()
        marks.append(float(mark))


    print(f"Average is {sum(marks)/len(marks):.2f}")
    print(f"Highest mark was {find_highest(marks)}")
        




if __name__ == "__main__":
    main()