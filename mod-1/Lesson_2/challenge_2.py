"""
Challenge 2 module. Compressed.
"""

def sum_implementation(*args) -> str:
    """
    Takes a given list of numbers and returns the sum as a str formatted to two decimal places.
    """
    return "${:.2f}".format(sum(args[0]))

def main():
    """
    Condensed main function.
    """
    # ask user for things + declare need vars
    prompts:list[str] = ["What is your monthly salary?", "what is your monthly cost of rent?", "what is the cost of groceries?"]
    variable_list:list = []
    subtracting:bool = False
    # iterate through the prompts.
    for prompt in prompts:
        i = float(input(prompt + "\n").strip("$"))
        # multiply i by -1 if subtracting so sum will remove instead of add
        i = i * -1 if subtracting else i
        subtracting = True
        # append to list.
        variable_list.append(i)
    # return value
    print(sum_implementation(variable_list), "is your spare money.")

if __name__ == "__main__":
    try:main()
    except ValueError: print('Not a number. Go away.')
    except Exception as e: print ("Woopsie. Goodbye!")