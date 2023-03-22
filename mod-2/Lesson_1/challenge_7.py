"""
traversal numbering
"""

def main():
    """
    Main function
    """
    # get word
    word = input("Please enter word\n")
    # process + output
    letters = [i for i in word]
    out_dict = {index:letter for (index, letter) in zip(range(len(letters)), letters)}
    for i in out_dict:
        print(f"Letter {i+1} is {out_dict[i]}")


if __name__ == "__main__":
    main()