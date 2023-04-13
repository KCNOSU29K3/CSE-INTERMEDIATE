#! /usr/bin/env python3


def main():
    """
    Main Function of program.
    """
    hear_joke = input("Do you want to hear a joke? [y/N]\n")

    if "y" not in hear_joke.lower():
        print("Goodbye.")
        exit()

    print("This programmer.")


if __name__ == "__main__":
    main()