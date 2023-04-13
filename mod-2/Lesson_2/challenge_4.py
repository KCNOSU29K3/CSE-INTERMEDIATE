#! /usr/bin/env python3


def main():
    """
    Main Function of program.
    """
    phone_list = [["name", "cell", "email"]]

    # add contacts
    while True:

        in_ = input("Please enter a new contact name.\nenter \"Done\" to exit.\n")

        if in_.lower() == "done":
            break

        name = in_
        cell = input("Cell phone number:")
        email = input("Email: ")
        appender = [name, cell, email]
        phone_list.append(appender)

    # check for name
    name = input("Please enter a name to look up.\n").lower()


    for contact in phone_list:
        if name == contact[0].lower():
            print("Found")
            print(contact)
            exit()
    

    print("Could not find name.")
    exit()


if __name__ == "__main__":
    main()