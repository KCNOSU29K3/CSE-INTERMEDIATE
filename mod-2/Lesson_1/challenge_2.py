"""
replace demo
"""

def main():
    """
    main function.
    """
    # variables
    words = """“Hire new field systems maintainer" was near the top of my to-do list, right under "uncover massive political conspiracy," "avenge Buffy's death," and "don't die.”"""

    # out + processing
    print(f"Original quote is: {words}")
    print(f"New quote is: {words.replace('conspiracy', 'solid plan')}")

if __name__ == "__main__":
    main()