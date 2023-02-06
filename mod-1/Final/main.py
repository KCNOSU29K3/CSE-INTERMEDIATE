#! /usr/bin/env python3
"""
A Phonebook system. requires `colorama`, `tqdm`, and `windows-curses` if on Windows.
"""

def auto_install(package):
    """
    Installs non-standard packages.
    
    ### Parameters

    `package` the name of the package.

    ### Returns

    `int` - 0.
    """

    if os.name == "nt":
        os.system(f"python -m pip install {package}")
        return 0
    else:
        os.system(f"python3 -m pip install {package}")
        return 0

import os

# installing other packages
non_standard_packages = ["colorama", "tqdm"]
# windows only import
if os.name == "nt":
    auto_install("windows-curses")

# install packages.
for package in non_standard_packages:
    auto_install(package)


from phonebook.phonebook import init_program
if __name__ == "__main__":
    init_program()