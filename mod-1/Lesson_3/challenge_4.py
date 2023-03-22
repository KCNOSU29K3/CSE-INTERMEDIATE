#!/usr/bin/env python3

import random
import string
from getpass import getpass
from decorators import timed


def generate_random_password(length):
    """
    Generates a random password with N length. Sample Space is 95 characters.
    """
    
    # generate a sample space
    sample_space = [i for i in string.ascii_letters + string.digits + string.punctuation]
    return_list = []

    # shuffle for entropy
    for i in range(10000):
        random.shuffle(sample_space)

    # generate password of N length
    for i in range(length):
        return_list.append(random.choice(sample_space))

        # shuffle again for more entropy
        for i in range(10):
            random.shuffle(sample_space)

    # format to string
    return "".join(return_list)


def password_dialog(use_random_pass:bool=False):
    """
    Password dialog for this challenge.
    """


    # set passphrase
    if not use_random_pass:
        password = "skynet"

    # get passphrase
    else:
        password = generate_random_password(240)

    # user gets 3 guesses
    for i in range(3):
        user_password = getpass()
        
        # correct, return to stop program from progressing
        if user_password == password:
            print("Authorized.")
            return
        
        print("Denied.")

    # exit

    print("Maximum amount of tries reached. Killing interpreter.")
    if use_random_pass:
        print(f"The randomly generated password was: {password}")

    return


# get preformance characteristics
@timed
def main():
    # decide if we should use an actual password
    use_random_gen = input('Use a randomly generated passphrase instead of the default for this exercise?\n').upper()


    # inform user of choice and set var
    if "N" in use_random_gen:
        print("Using preset password for this activity.")
        use_random_bool = False
    elif "Y" in use_random_gen:
        print('Using cryptographically strong password for this activity.')
        use_random_bool = True
    else:
        print("Invalid content detected. Assuming No.")
        use_random_bool = False

    # execute
    password_dialog(use_random_bool)

if __name__ == "__main__":
    null, ns, s = main()
    # performance characteristics
    print(f"Program ran in {ns} nanoseconds | {s} seconds.")