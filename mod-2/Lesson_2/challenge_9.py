#! /usr/bin/env python3


def replace(orginal:str, old:str, new:str) -> str:
    """
    Replaces all instances of an old string with a new string.
    """
    return orginal.replace(old, new)


def main():
    """
    Main Function of program.
    """
    word = input("What is the phrase to parse?\n")
    old = input("What is the word to be replaced?\n")
    new = input("What is the word to replace with?\n")
    print("Return phrase is:")
    print(replace(word, old, new))


if __name__ == "__main__":
    main()