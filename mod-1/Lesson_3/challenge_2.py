#!/usr/bin/env python3

from decorators import timed

def i():
    _exit = False
    while not (_exit):
        in_ = input("EXIT? [Y/N]\n").upper()
        if "N" in in_: continue
        if "Y" in in_: _exit = True ; print("Exiting")
        else: print("Invalid response")


@timed
def main():
    i()

if __name__ == "__main__":
    null, ns, s = main()

    print(f"Function ran in {ns} nanosecnds | {s} seconds.")