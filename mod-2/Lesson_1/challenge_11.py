"""

"""

import string

def main():
    """
    main function
    """
    key = input("Enter a key\n")[0]
    if key in string.ascii_uppercase:
        print("key is uppercase.")
    elif key in string.ascii_lowercase:
        print("key is lowercase.")
    elif key in string.punctuation:
        print("Key is punctuation.")
    elif key in string.digits:
        print("key is numeric.")


if __name__ == "__main__":
    main()