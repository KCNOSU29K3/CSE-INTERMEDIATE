#! /usr/bin/env python3


def main():
    """
    Main Function of program.
    """
    # list comp
    words = ["adopt", "bake", "beam", "confide", "grill", "plant", "time", "wave", "wish"]
    past_tense = [i+"ed" for i in words if i[-1] != "e"] + [i+"d" for i in words if i[-1] == "e"]
    
    # out
    print("Past tense words are:")
    for i in past_tense:
        print(i)
    pass


if __name__ == "__main__":
    main()