"""
traversal to count specific character
"""

from textwrap import dedent

def main():
    """
    
    """
    text = input("Please enter your full name\n").lower()
    occurrences = text.count("e")
    percentage = occurrences / len(text) * 100
    out = f"""
    There are {occurrences} occurrences of e.
    This comprises ~ {percentage:.2f}% of all characters in your name.
    """
    print(dedent(out))



if __name__ == "__main__":
    main()