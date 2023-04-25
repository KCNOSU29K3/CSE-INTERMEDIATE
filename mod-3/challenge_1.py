#! /usr/bin/env python3
import os
import zipfile
from base64 import decodebytes


file_data = [
b"""
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
AAEAAQA2AAAAcQYAAAAA
"""
]


class InvalidFileOperation(Exception):


    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class File_Handler:
    """
    Wrapper class around Python File Operations.

    If instantiated with mode \"x\", the handler will create the 
    file and then switch to read only mode.
    """

    def __init__(self, file:str, mode:str = "r") -> None:


        self.mode = mode
        self.file_location = file

        # file handling variables
        self.supports_bytes = False
        self.supports_read, self.supports_write = self.__define_supports(self.mode)

        self.__check_file_exists()

        self.file_object = open(self.file_location, self.mode)


    # file methods

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

        `InvalideFileOperation` - The current file mode does not support read.
        """


        # raise error if reading is not supported
        if self.supports_read is not True:
            raise InvalidFileOperation(f"File Mode \"{self.mode}\" does not support read.")

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


    def write_file(self, content:str|bytes):
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

        # convert
        if self.supports_bytes:
            content = bytes(content)

        # raise error if write is not supported
        if self.supports_write is not True:
            raise InvalidFileOperation(f"File Mode {self.mode} does not support write.")
        
        # execute write
        self.file_object.write(content)
        
        return 0


    # setter methods

    def set_encoding(self, encoding:str):
        """
        Changes the file object encoding.

        ### Parameters

        `encoding` - The encoding to switch to.

        ### Parameters

        `int` - A return code of 0.
        """
        self.file_object.close()
        self.file_object = open(self.file_location, self.mode, encoding=encoding)
        return 0


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
            with open(new_file_name, "x") as file:
                pass

        self.file_location = new_file_name
        
        # check if file exists
        self.__check_file_exists()

        # shift out file objects
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

        # identify read/write support
        self.supports_read, self.supports_write = self.__define_supports(new_mode)
        

        # shift out file objects
        self.file_object.close()
        self.file_object = open(self.file_location, self.mode)
        return 0


    def __check_file_exists(self):
        """
        Private function that checks if a given file path exists.

        ### Raises

        `FileNotFoundError` - The file does not exist.

        ### Returns:

        `int` - An integer returncode of 0.
        """
        if not os.path.exists(self.file_location):
            raise FileNotFoundError
        return 0
        

    # private methods


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

        self.file_object = open(self.file_location, "r")
        self.mode = "r"
        self.supports_read, self.supports_write = self.__define_supports("r")

        return 0


    def __define_supports(self, mode:str) -> tuple:
        """
        Private method that identifies what operations 
        a given file mode will support.

        ### Parameters

        `mode` the mode to check, as a string.

        ### Returns

        `(bool, bool)` - The read/write supports of the mode, respectively.

        `(None, None)` - The File mode is not valid.
        """
        write_operators = ["w", "a", "wb", "ab"]
        read_operators = ["r", "rb"]
        
        if "b" in mode:
            self.supports_bytes = True

        # decision tree
        if mode == "x":
            self.__create_file(self.file_location)
            return False, False

        elif "+" in mode:
            # read and write
            return True, True
        
        elif mode in write_operators:
            # read and write
            return False, True
        
        elif mode in read_operators:
            # read and write
            return True, False
        
        else:
            return None, None


    # define destructor to close file before object 
    # destruction
    def __del__(self):
        """
        Destructor method that ensures the file object is closed 
        when the class object reference count drops to 0.
        """
        if not hasattr(self, "file_object"):
            self.file_object.close()


def generate_data_if_not_existent():
    """
    Generates the data for the drawing if it cannot be found.
    """
    # define a file handler object
    file_handler = File_Handler("./.zipped_data.zip", "x")
    # build zip file
    file_handler.change_file_mode("wb+")
    file_handler.write_file(decodebytes(file_data[0]))


    # delete file handler to allow zipfile to open it
    del file_handler

    # unzip file
    zip_handler = zipfile.ZipFile("./.zipped_data.zip")
    zip_handler.extractall()

    # clean up
    del zip_handler
    os.remove("./.zipped_data.zip")


def main():
    

    if not os.path.exists("./data.txt"):
        generate_data_if_not_existent()

    if not os.path.exists("./different_folder"):
        os.mkdir("./different_folder")


    system_file_handler = File_Handler("./data.txt")
    lines = system_file_handler.read_file(return_lines=True)
    system_file_handler.goto(0)
    content = system_file_handler.read_file()

    for i in lines:
        print(i)

    
    system_file_handler.change_file_name("./different_folder/new_data.txt", True)
    system_file_handler.change_file_mode("w+")
    system_file_handler.write_file(content)

    lines = system_file_handler.read_file()


    for i in lines:
        print(i)

    


if __name__ == "__main__":
    main()
