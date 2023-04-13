#! /usr/bin/env python3


def main():
    """
    Main Function of program.
    """
    # data manipulation
    data_structure = []
    print(data_structure)
    data_structure.append(76)
    print(data_structure)
    data_structure.append(92.3)
    print(data_structure)
    data_structure.append("hello")
    print(data_structure)
    data_structure = data_structure + [True, 4, 76]
    print(data_structure)
    data_structure.append("apple")
    print(data_structure)
    data_structure.append(76)
    print(data_structure)
    data_structure.insert(3, "cat")
    print(data_structure)
    data_structure.insert(0, 99)
    print(data_structure)
    hello_index = data_structure.index("hello")
    print(f"{hello_index} is index of 'hello'")
    amount_of_76 = data_structure.count(76)
    print(f"there are {amount_of_76} amounts of 76 in list.")
    data_structure.remove(76)
    print(data_structure)
    true_index = data_structure.index(True)
    data_structure.pop(true_index)
    print(data_structure)

    pass


if __name__ == "__main__":
    main()