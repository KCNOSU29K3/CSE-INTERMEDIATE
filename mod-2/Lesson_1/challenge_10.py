"""
Character in name
"""

def find_letter(string:str, char:str):
    """
    Locates first index of `char` in `string`.
    returns -1 if not found.
    """
    string = [i for i in string]
    try: index = string.index(char) ; return index
    except ValueError: return -1
    pass


def main():
    """
    main function
    """
    letter = input("Please enter your letter\n").lower()
    name = input("please enter the name to index\n")
    index = find_letter(name, letter)
    if index == -1:
        print("Letter does not exist.")
        exit()
    print(f"Letter found at index {index} | postion {index + 1}")
    



if __name__ == "__main__":
    main()