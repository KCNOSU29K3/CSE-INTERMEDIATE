"""
Format demo
"""

def main():
    """
    main function
    """
    # GET DATA
    name = input("What is your name?\n")
    age = input("What is your age?\n")
    fav_food = input("What is your favorite food?\n")

    # create list to iterate and print over
    out = [
        "Your name is {}\n".format(name),
        "You are {} years old\n".format(age),
        "Your favorite food is {}".format(fav_food)
    ]

    # out
    for i in out:
        print(i)



if __name__ == "__main__":
    main()