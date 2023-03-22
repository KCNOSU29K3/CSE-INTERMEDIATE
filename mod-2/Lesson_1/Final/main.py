"""
String to NATO Phonetic converter.
"""
# imports
import os
import string
from textwrap import dedent

def clear(function):
    """
    Runs a given function, clearing the terminal before and after
    """

    def wrapper(*args, **kwargs):
        os.system("cls" if os.name == "nt" else "clear")
        function(*args, **kwargs)
        os.system("cls" if os.name == "nt" else "clear")

    return wrapper


def generate_converter():
    """
    Returns a conversion dictionary, covering numbers, uppercase/lowercase letters, and punctuation.

    Requires no parameters.
    """


    # construct lists for dictionary later
    nato_numbers = ["Zee-ro", "Wun", "Too", "Tree", "Fow-er", "Fife", "Six", "Sev-en", "Ait", "Niner"]
    nato_phonetics = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliett", "Kilo", "Lima", "Mike", "November", "Oscar", "Papa", "Quebec", "Romeo", "Sierra", "Tango", "Uniform","Victor", "Whiskey", "X-ray", "Yankee", "Zulu"]
    nato_phonetics_lower = [i.lower() for i in nato_phonetics]
    

    #  convert LiteralString to list
    letters = [i for i in string.ascii_letters]
    digits = [i for i in string.digits]
    letters = letters + digits


    # join lists
    nato_phonetics = nato_phonetics_lower + nato_phonetics + nato_numbers


    # dictionary comprehension magic
    # essentially the same as a list comprehension, but iterates over tuples instead to create a dictionary
    # zip returns a tuple of 2 elements in two seperate lists of N index. Zip is also an iterator, which allows
    # for the loop.
    converter = {letter: phonetic for (letter, phonetic) in zip(letters, nato_phonetics)}
   

    # cover conversion punctuation
    for i in string.punctuation:
        converter[i] = i


    return converter


def intro():
    """
    Prints out the introductory message.
    """
    out = """
    This program is a tool that allows for the conversion of the english alphabet to 
    standard NATO Phonetics.
    """
    print(dedent(out))
    pass


@clear
def main():
    """
    Main function.
    """

    intro()

    # Generate conversion table
    conv = generate_converter()

    # get sentence
    sentence = input("Please enter the phrase to encode.\n")
    print()
    # this will be used for printing out the full message later.
    list_ = []

    # iterate through sentence
    for i in sentence:

        # space handling
        if i == " ":
            print()
            continue

        # corrosponding phonetic
        print(f"{i} : {conv[i]}")

        # append to list
        list_.append(conv[i])

    # output
    print("\nFull Sentence:\n")
    print(" ".join(list_))
    
    # decide whether or not to show conversion table
    show_conversion_table = True if "y" in input("\nShow Conversion table? [y/N]\n") else False
    
    if not show_conversion_table: print("\nExiting...") ; return
    print("\nConversion Table")

    # iterate through dictionary
    for i in conv:
        print(f"{i} : {conv[i]}")

    input("Press Enter to Exit.\n")


if __name__ == "__main__":
    main()