#! /usr/bin/env python3
import os
import sys
import json
import base64
import string
import warnings
from textwrap import dedent

class InvalidFileOperation(Exception):


    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class File_Manager:
    """
    A Wrapper class for the `File_Handler` class that
    manages multiple files at once.
    """
    
    def __init__(self, file_id_type:type) -> None:
        self.expects_id_type = file_id_type

        self.file_registry:dict[type, File_Handler] = {}


    def add_file(self, id:type, file_path:str, mode:str = "r"):
        """
        Adds a file to the internal registry.
        """

        if type(id) != self.expects_id_type:
            raise TypeError("Invalid identifier used for file object management.")

        file_object = File_Handler(file_path, mode)

        self.file_registry[id] = file_object


    def retrieve_file(self, id:type):
        """
        Retrieves a file from the registry.
        """

        if type(id) != self.expects_id_type or type(id) != list[self.expects_id_type]:
            raise TypeError("Invalid identifier used for file object look up.")

        if self.file_registry.get(id) is None:
            return None
        
        return self.file_registry[id]


    def remove_file(self, id):
        """
        Removes a file from the internal registry.
        """

        if type(id) != self.expects_id_type:
            raise TypeError("Invalid identifier used for file object deletion")
        
        if self.file_registry.get(id) is None:
            return None
        
        self.file_registry.pop(id)


    def open_file_list(self, filepath_list:list[str], mode_list:list[str], id_list:list[type]):
        """
        Iterates through two lists to open multiple file objects at once.

        `filepath_list` - The list of filepaths to open.

        `mode_list` - The list of modes to open the filepaths with.

        `id_list` - the ids to give the newly created file objects.

        #### Raises

        `ValueError` - The lengths of the parameters are different and the write could not be executed.
        """

        if not self.verify_list_lengths([filepath_list, mode_list, id_list]):
            raise ValueError(
                "Parameter list length mismatch.\n"
                f"Expected length {len(filepath_list)}\n"
                f"Got lengths: {len(filepath_list)}|{len(mode_list)}|{len(id_list)}"
                )


        for i in range(len(filepath_list)):
            self.add_file(id_list[i], filepath_list[i], mode_list[i])


    def write_to_file(self, fileID:type, content:str|bytes|list, flush:bool = True, lines:bool=False):
        """
        Writes to a given file.

        #### Parameters

        `fileID` - The ID of the file to write to.

        `Content` - The content to write to the file.

        `Flush` - Boolean value that controls flushing of the data from the buffer.

        `Lines` - Boolean value that controls `writelines()` usage.

        ### Returns

        `-1` - The given ID for the file is invalid.
        """
        if self.file_registry.get(fileID) is None:
            return -1
        
        file_object = self.file_registry[fileID]

        file_object.write_file(content, flush, lines)


    def write_to_file_list(self, content:list[str|bytes|list], filepaths:list[str], ids:list[type]):
        """
        writes to a list of files in series.

        #### Parameters

        `content` - A list of the content to write to the files.

        `filepaths` - The list of files to write to.

        `ids` - The list of ids to give the newly written files.

        #### Raises

        `ValueError` - The 3 parameters have mismatching lengths. 
        """

        if not self.verify_list_lengths([content, filepaths, ids]):
            raise ValueError (
                "Parameter list length mismatch.\n"
                f"Expected length {len(content)}.\n"
                f"Got lengths {len(content)}|{len(filepaths)}|{len(ids)}"
            )
        pass


    def change_file_mode(self, id:type, new_mode:str):
        """
        Changes the file mode of a given file.

        #### Parameters

        `id` - the given id for the file.

        `new_mode` - The new mode to switch to, as a string.

        #### Raises

        `KeyError` - The given file ID does not exist.

        #### Returns
        
        `0` - Default return value.
        """
        if self.file_registry.get(id) is None:
            raise KeyError("Invalid file ID.")
        self.file_registry[id].change_file_mode(new_mode)
        return 0


    def clear_file(self, id):
        """
        Completely truncates a given file.

        #### Parameters

        `id` - A file id.

        #### Returns

        `-1` - The given file id is invalid.
        """
        if self.file_registry.get(id) is None:
            return -1
        self.file_registry[id].truncate()


    def verify_list_lengths(self, lists_to_verify:list[list]):
        """
        Ensures that a given set of lists are of the same size.

        #### Parameters

        `lists_to_verify` - 1 Monolithic list containing the lists to be checked.

        #### Returns

        `bool` - Whether or not the lists are the same length.
        """

        # spooky stack overflow magic
        if len(set(map(len, lists_to_verify))) == 1:
            return True
        return False


    def read_file(self, id, len_=0, lines=False, index:int = None):
        """
        Reads the contents of a given file.

        #### Parameters

        `id` - The id of the file to read from.

        `len_` - The amount of data to read from the file.

        `lines` - Whether or not to return the data as a set of lines.

        `index` - Where to start reading from the file.

        #### Returns
        
        `list[str|bytes]` - The specified contents of the file, as a set of lines.

        `str|bytes` - The specified contents of the file.

        #### Raises

        `KeyError` - The given file id does not exist.
        """
        if self.file_registry.get(id) is None:
            raise KeyError("Invalid file ID.")
        return self.file_registry[id].read_file(len_, lines, index)


    def __del__(self):
        """
        We dereference the internal registry, triggering the file_handlers to close their files.
        """
        del self.file_registry


class File_Handler:
    """
    Wrapper class around Python File Operations.

    If instantiated with mode \"x\", the handler will create the 
    file and then switch to read only mode.
    """


    def __init__(self, file:str, mode:str = "r", encoding:str = "utf-8") -> None:

        self.mode = mode
        self.file_location = file
        self.supports_bytes = True if "b" in mode else False
        
        if self.mode == "x":
            self.__create_file(self.file_location)

        # file handling variables

        self.__check_file_exists()
        self.encoding = encoding
        self.file_object = open(self.file_location, self.mode)

    # file methods


    def find_index(self):
        """
        Returns the current index of the file reader.

        ### Returns

        `int` - An integer representing the current position of the file.
        """
        return self.file_object.tell()


    def expose_file_object(self):
        """
        Exposes the internal file object to the outside world.

        As a general use case, only do this if you need to pass the object to 
        another function that consumes a file object.
        """
        return self.file_object


    def read_file(self, len_:int = 0, return_lines:bool = False, index:int = None):
        """
        Reads and returns the content from the current file object.

        ### Parameters

        `len_` - An optional integer parameter indicating how much
        of the file contents to read. The default is 0, which reads the
        entire file.

        `return_lines` - An optional boolean parameter indicating whether
        or not to return the file as an array of lines. If `len_` is specified,
        the returned list will be of `len_` length.

        ### Returns

        `list[str]` - A list of lines from the file.

        `str` - The contents of the file.

        `list[bytes]` - A list of lines from the file, represented as bytes.

        `bytes` - The contents of the file, represented as bytes.

        ### Raises

        `InvalidFileOperation` - The current file mode does not support read.
        """

        # raise error if reading is not supported
        if self.file_object.readable() is not True:
            raise InvalidFileOperation(f"InvalidFileOperation: File Mode \"{self.mode}\" does not support read.")

        # return only a slice of the file

        if index is not None:
            self.file_object.seek(index)


        if len_ != 0:
            
            if return_lines:
                return self.file_object.readlines(len_)

            return self.file_object.read(len_)
        
        # return file
        else:
            if return_lines:
                return self.file_object.readlines()

            return self.file_object.read()   


    def write_file(self, content:str|bytes|list, flush:bool = True, lines=False):
        """
        Writes content to the file.

        Will auto-convert content to bytes if file mode supports bytes.

        ### Parameters

        `content`: The content to write to the file. Must be convertible to 
        bytes and/or strings.

        ### Returns

        `int` - A return code of 0.

        ### Raises

        `InvalidFileOperation` - The current mode does not support writing.
        """

        if isinstance(content, list) and not lines:
            raise TypeError("Content was given as a list but flag for outputting lines is false.")

        # convert
        if isinstance(content, list) and self.supports_bytes:
            content = [bytes(i, self.encoding) for i in content]

        elif isinstance(content, str) and self.supports_bytes:
            content = bytes(content, self.encoding)
        
        elif isinstance(content, bytes) and not self.supports_bytes:
            try:
                content = str(content, self.encoding)
        
            except UnicodeDecodeError:
                content = base64.encodebytes(content)
                warnings.warn(f"Encoding bytes to {self.encoding} failed. Encoding in Base 64.", EncodingWarning)


        # raise error if write is not supported
        if self.file_object.writable() is not True:
            raise InvalidFileOperation(f"InvalidFileOperation: File Mode {self.mode} does not support write.")
        
        # execute write
        if lines:
            self.file_object.writelines(content)
        else:
            self.file_object.write(content)


        if flush:
            self.file_object.flush()


        return 0


    # setter methods


    def goto(self, index:int):
        """
        Shifts the file reading index to a specified location.

        ### Parameters

        `index` - The index to shift the reading index to.

        ### Returns

        `int` a return code of 0.
        """
        self.file_object.seek(index)
        return 0


    def set_encoding(self, encoding:str):
        """
        Changes the file object encoding.

        ### Parameters

        `encoding` - The encoding to switch to.

        ### Parameters

        `int` - A return code of 0.
        """
        self.file_object.flush()
        self.file_object.close()
        self.file_object = open(self.file_location, self.mode, encoding=encoding)
        return 0


    def truncate(self):
        """
        Completely truncates the file.

        Does not return a value.
        """
        self.file_object.truncate(0)
        self.goto(0)



    def change_file_name(self, new_file_name:str, create_if_non_existent:bool = False):
        """
        Changes the file name. This loses access to the 
        previous file. 

        ### Parameters

        `new_file_name` - The name of the new file as a string.

        ### Returns

        `int` - A return code of 0.

        ### Raises

        `FileNotFoundError` - The file does not exist. If this
        error is caught and handled, the file name this wrapper 
        points to must be changed in order to be properly used. 
        """

        if create_if_non_existent and not os.path.exists(new_file_name):
            self.__create_file(new_file_name)


        self.file_location = new_file_name
        
        # check if file exists
        self.__check_file_exists()

        # shift out file objects
        self.file_object.flush()
        self.file_object.close()
        self.file_object = open(self.file_location, self.mode)

        return 0


    def change_file_mode(self, new_mode:str):
        """
        Changes the mode of the file object this wrapper points to.

        ### Parameters

        `new_mode` - A string indicating the new mode of the file. 
        Analogous to Python file operators.

        ### Returns

        `int` - A integer returncode of 0.
        """
        
        # assign new mode
        self.mode = new_mode

        self.supports_bytes = True if "b" in new_mode else False

        # shift out file objects
        self.file_object.flush()
        self.file_object.close()
        self.file_object = open(self.file_location, self.mode)
        return 0


    # private methods


    def __check_file_exists(self):
        """
        Private function that checks if a given file path exists.

        ### Raises

        `FileNotFoundError` - The file does not exist.

        ### Returns:

        `int` - An integer returncode of 0.
        """
        if "w" in self.mode or "a" in self.mode:
            return 0
        if not os.path.exists(self.file_location):
            if not hasattr(self, "file_object"):
                self.file_object = open(f"{__file__}", "r")
            raise FileNotFoundError(f"FileNotFoundError: File \"{self.file_location}\" Does not exist.")
        return 0
 

    def __create_file(self, file_location:str):
        """
        Private method for the "x" file operator.

        ### Parameters

        `file_location` - The location of the file to be created.

        ### Returns

        `int` - An integer returncode of 0.
        """
        
        with open(file_location, "x") as file:
            pass
        self.mode = "r"
        self.supports_bytes = False


    # destruction
    def __del__(self):
        """
        Destructor method that ensures the file object is closed 
        when the class object reference count drops to 0.
        """
        # checking for attribute since it will not be generated if 
        # we attempt to generate a file with "x" operator and it already exists.
        # that will raise an UnraisableExceptionWarning and spit a traceback to the
        # console, which we don't want to do.
        if hasattr(self, "file_object"):
            self.file_object.flush()
            self.file_object.close()


class Inventory_Manager:


    def __init__(self) -> None:

        self.inventory = {}


    def get_inventory(self):
        """
        Returns the internal inventory.

        Takes no parameters.
        """
        return self.inventory


    def update_inventory(self, restock_amount:int, item_id:type):
        """
        Restocks a given product be a given amount.

        #### Parameters

        `restock_amount` - The amount to restock the given item by.

        `item_id` - The id of the item, as a given type.
        """
        
        # check id exists.
        if self.inventory.get(item_id) is None:
            raise KeyError("Key for value not found.")

        original_data = self.inventory[item_id]
        self.inventory[item_id] = [original_data[0], restock_amount, original_data[2]]




    def generate_product_base(self, items_list:list[str], prices:list[str], item_ids:list[type]):
        """
        Generates a dictionary for the product base.

        mapping:

        item_id -> (item name, default stock (0), price)

        #### Parameters

        `items_list` - The list of item names, as strings.

        `prices`  - The list of item prices, as strings.

        `item_ids` - The item ids, as a set of types.
        """

        # stackoverflow magic to detect if all list lengths are the same.
        if len(set(map(len, [items_list, prices, item_ids]))) != 1:
            raise ValueError(
                "Parameter list length mismatch.\n"
                f"Expected length {len(items_list)}\n"
                f"Got lengths: {len(items_list)}|{len(prices)}|{len(item_ids)}"
                )
        

        output = {}

        for i in range(len(items_list)):
            output[item_ids[i]] = (items_list[i], 0, prices[i])

        # return and store for easier data manipulation.
        self.inventory = output
        return output


    def parse_input(self, input_:str):
        """
        parses input.

        ### Parameters

        `input_` - The input to parse, as a string.
        """
        input_ = input_.strip()
        input_ = input_.replace(", ", ",")        
        return input_.split(",")


def clear():
    """
    Small function that clears stdout.
    """
    os.system("cls" if os.name == "nt" else "clear")


def restart():
    """
    Small function that restarts the program as a whole.
    """
    os.execv(sys.executable, ["python" if os.name == "nt" else "python3"] + sys.argv)


def verify_int_convertible(string_:str):
    """
    Small function that ensures a given string can
    be converted to an integer.
    """
    good_chars = [i for i in string.digits]

    for char in string_:
        if char not in good_chars:
            return False
    return True


def verify_float_convertible(string_:str):
    """
    small function that ensures a string can be converted 
    to a floating point value.
    """
    good_chars = [i for i in string.digits] + ["."]

    for char in string_:
        if char not in good_chars:
            return False
    return True


def base(inventory_manager:Inventory_Manager, system_file_manager:File_Manager):
    """
    Queries the user for the stock base. Requires an existent `Inventory_Manager` and
    `File_Manager` to share data, and returns None.

    #### Parameters

    `inventory_manager` - An inventory manager class, used to store and manipulate data.

    `system_file_manager` - A file manager class, used to interact with the filesystem.
    """

    # query user for the names first
    while True:
        names = input("Please enter product names separated with commas.\n")
        names = inventory_manager.parse_input(names)    
        clear()
        for i in names:
            print(i)
        should_restart = input("Are these item names correct? [Y/n]\n")
        if "n" not in should_restart:
            break
        
    
    # price grabbing
    while True:
        
        clear()
        # so the user has a better idea of what they are pricing
        for i in names:
            print(i)

        # ask and parse input
        prices = input("Please enter prices for items, separated with commas and without symbols.\n")
        prices = inventory_manager.parse_input(prices)
        clear()

        # ensure that we can convert to float for these prices
        # we do this here since it saves us a headache down the road and 
        # allows the user to correct their errors.
        continue_ = False
        for i in prices:
            if not verify_float_convertible(i):
                print("These prices are invalid. Please do not include any symbols in the prices.")
                input("Press Enter to continue.\n")
                continue_ = True
            print(i)

        if continue_:
            continue
        
        # ensure that these prices are the ones they want
        restart_prompt = input("Are these the correct prices? [Y/n]\n")
        if "n" in restart_prompt:
            continue

    # create a dictionary for output use

        # this magic was obtained from stackoverflow and checks that both lists
        # are the same size
        if len(set(map(len, [names, prices]))) != 1:
            print("You have provided an incorrect amount of prices.")
            print(f"Please reenter the list with {len(names)} items.")
        else:
            break
    
    clear()
    # final check
    print_out_dict = {name: price for (name, price) in zip(names, prices)}
    for name, price in print_out_dict.items():
        print(f"{name}: {price}")
    should_restart = input("Is this list correct? [Y/n]\n")
    if "n" in should_restart:
        restart()

    # list of item ids for the base dict
    item_ids = [str(i) for i in range(0, len(names))]

    # output base
    product_base_dict = inventory_manager.generate_product_base(names, prices, item_ids)
    system_file_manager.write_to_file(0, json.dumps(product_base_dict, indent=4))


def restock(inventory_manager:Inventory_Manager, system_file_manager:File_Manager):
    """
    Queries the user for new stock to save. Requires an `Inventory_Manager` and 
    `File_Manager` to handle data.

    #### Parameters

    `inventory_manager` - An inventory management class that handles the inventory.

    `system_file_manager` - A file manager that handles file interactions.
    """
    while True:
        clear()
        # output current system data
        product_base_dict = inventory_manager.get_inventory()
        for item_id, data in product_base_dict.items():
            print(f"product: {data[0]}: Stock: {data[1]}: System ID: {item_id}")

        print("Please enter an id for a product.")
        print("Enter CTRL+D (CTRL+Z on Windows) or enter \"EXIT\" to continue.")

        # try/except to catch CTRL+D
        try:
            item_id = input()

            # check for break conditions
            if item_id.lower() == "exit":
                break

            if product_base_dict.get(item_id) is None:
                print("Invalid system ID. Cannot Retrieve.")
                input("Press enter to continue.\n")
                continue

            restock_amount = input("Please enter the amount to restock by.\n")
            
            # ensure we have a usable input 
            if verify_int_convertible(restock_amount):
                inventory_manager.update_inventory(int(restock_amount), item_id)
            else:
                # inform user that their input was bad
                print(f"{restock_amount} is not a number.")
                print("Ignoring...")
                input("Press Enter to continue.")
                continue
        except EOFError:
            break

        # output
        system_file_manager.clear_file(1)
        system_file_manager.write_to_file(1, json.dumps(inventory_manager.get_inventory(), indent=4))


def purchase(inventory_manager:Inventory_Manager, system_file_manager:File_Manager):
    """
    Queries the user for items to purchase.
    Keeps track of money spent.
    """

    # purchases defined outside of loop to keep the data
    purchases = []
    while True:
        clear()
        # inform the user of what this us
        print("Purchase Window")
        # display items

        # output items + capital
        inventory = inventory_manager.get_inventory()
        for id, data in inventory.items():
            print(f"{data[0]}: Costs: {data[2]}: Stock: {data[1]}: System ID: {id}")

        print(f"Current capital: ${sum(purchases):.2f}")

        print("Please enter an id for a product.")
        print("Enter CTRL+D (CTRL+Z on Windows) or enter \"EXIT\" to continue.")
        try:

            # ensure we have usable input and check guard clauses
            item_id = input()
            
            if item_id.lower() == "exit":
                break
            
            if inventory.get(item_id) is None:
                print("Invalid system ID. Cannot Retrieve.")
                input("Press enter to continue.\n")
                continue
            purchase_amount = input("Please enter amount to purchase.\n")

            if not verify_int_convertible(purchase_amount):
                print(f"{purchase_amount} is not a number.")
                print("Ignoring...")
                continue
            
            purchase_amount = int(purchase_amount)
            stock_of_item = inventory[item_id][1]
        

            if stock_of_item < purchase_amount:
                print("Current stock does not allow for this purchase.")
                input("Press enter to continue.\n")
                continue

            # we do no checks on the prices since that was handled in the base function
            price = float(inventory[item_id][2])*purchase_amount
            purchases.append(price)

            # update the inventory
            inventory_manager.update_inventory(int(stock_of_item-purchase_amount), item_id)
        except EOFError:
            break

        # output
        # clear the file so that writing again will not append to already existent data.
        system_file_manager.clear_file(2)
        system_file_manager.write_to_file(2, json.dumps(inventory_manager.get_inventory(), indent=4))
    
    # we return the money gained for the end function.
    return f"{sum(purchases):.2f}"


def end(system_file_manager:File_Manager, money_earned:str):
    """
    Ending function that allows the user to access any one of the 3 files.
    Requires a `File_Manager` to access files.
    """
    clear()
    print("What file Do you want to access?")
    print("Base Stock (0)")
    print("Restock (1)")
    print("Business Quarter (2)")

    chosen_file = input()


    def output_data(file_ID):
        """
        Small internal function to reduce code needed for output.
        """
        system_file_manager.change_file_mode(file_ID, "r")
        system_data = json.loads(system_file_manager.read_file(file_ID))
        for item_ID, data in system_data.items():
            print(dedent(
                f"""
                ~~~~~~~~~~~~~~
                System Item ID: {item_ID}
                Item Name: {data[0]}
                Item Stock: {data[1]}
                Item Price: {data[2]}
                ~~~~~~~~~~~~~~j
                """
            ))
        print(f"Capital earned during operation: ${money_earned}")

    # simple match statement to find output.
    match chosen_file.lower():
        
        case "0":
            output_data(0)
        case "1":
            output_data(1)
        case "2":
            output_data(2)
        case "base stock":
            output_data(0)
        case "restock":
            output_data(1)
        case "business quarter":
            output_data(2)
        case _:
            print("Invalid Identifier.")
            print("Press Enter to continue.")
            input()
            end(system_file_manager, money_earned)


def main():
    """
    Main function of program.
    """

    # create required data
    system_file_manager = File_Manager(int)
    inventory_manager = Inventory_Manager()

    output_files = ["product_base.json", "restock_update.json", "business_quarter.json"]
    output_modes = ["w+"]*3
    output_ids = [i for i in range(0, 3)]

    system_file_manager.open_file_list(output_files, output_modes, output_ids)

    # main program
    base(inventory_manager, system_file_manager)
    restock(inventory_manager, system_file_manager)
    capital = purchase(inventory_manager, system_file_manager)
    end(system_file_manager, capital)
    

if __name__ == "__main__":
    main()