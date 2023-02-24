def i ():
    _exit = False
    while not (_exit):
        input = ("EXIT? [Y/N]\n").upper()
        if "N" in input: continue
        if "Y" in input: _exit = True
        else: print("Invalid response")