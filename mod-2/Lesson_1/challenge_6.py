"""
Word sorter
"""

def main():
    """
    Compact word ordering function

    how it works:
    get words from user

    add words to list

    sort list. This works because the list sort invokes lexical ordering.
    """
    w1 = input("First word:\n")
    w2 = input("Second word:\n")
    w3 = input("Third word:\n")
    list_ = [w1, w2, w3] ; list_.sort()
    print(f"First word is: {list_[0]}\nSecond word is: {list_[1]}\nThird word is: {list_[2]}")


if __name__ == "__main__":
    main()