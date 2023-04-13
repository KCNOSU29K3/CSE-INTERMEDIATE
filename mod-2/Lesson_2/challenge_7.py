#! /usr/bin/env python3


def script():
    """
    only here to comply with requirements
    """
    print("Enter Marks. Enter \"done\" when finished.")
    marks = []
    while True:
        mark = input("")
        if mark.lower() == "done": break
        marks.append(float(mark))
    marks.sort(reverse=True)
    return [marks, round(sum(marks)/len(marks), 2), marks[0]]


def main():
    """
    Main Function of program.
    """
    try:
        i = script()
        print("marks are:")
        for i_ in i[0]:
            print(f"{i_:.2f}")
        print(f"Average is: {i[1]:.2f}\nHighest was: {i[2]:.2f}")
    except ValueError:
        print("Please enter numbers only.")
    pass


if __name__ == "__main__":
    main()