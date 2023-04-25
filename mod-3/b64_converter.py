from base64 import encodebytes
import logging
import os



class InvalidFileOperation(Exception):


    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class File_Handler:
    """
    Wrapper class around Python File Operations.
    """

    def __init__(self, file:str, mode:str = "r") -> None:
        
        self.mode = mode
        self.file_location = file

        if not os.path.exists(self.file_location):
            raise FileNotFoundError

        # file handling variables
        self.supports_bytes = False
        self.supports_read, self.supports_write = self.__define_supports(mode)


        self.file_object = open(self.file_location, mode)


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


    def read_file(self, len_:int = 0, return_lines:bool = False):
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
        if len_ != 0:
            
            if return_lines:
                return self.file_object.readlines(len_)

            return self.file_object.read(len_)
        
        # return file
        else:
            if return_lines:
                return self.file_object.readlines()

            return self.file_object.read()   


    def write_file(self, content):
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

    
    def change_file_name(self, new_file_name:str):
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
        if not os.path.exists(self.file_location):
            if self.mode == "x":
                self.__create_file()
                return 0
            raise FileNotFoundError
        

    # private methods


    def create_file(self, file_location):
        """
        Private method for the "x" file operator.
        """
        
        with open(file_location, "w") as file:
            pass

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
            self.__create_file()
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
        self.file_object.close()


def main():
    """
    Main file
    """
    for root, dirs, files in os.walk(os.curdir):
        for file in files:
            if not file.endswith(".zip"):
                continue
            print(os.path.join(root, file))
    file_name = input("Please select the file you wish to encode\n")
    out_file = input("Please selct the name of the file to output to\n")

    file_handler = File_Handler(file_name, "rb")
    file_contents = file_handler.read_file()
    print(file_contents)
    file_handler.create_file(out_file)
    file_handler.change_file_name(out_file)
    file_handler.change_file_mode("wb")
    file_handler.write_file(encodebytes(file_contents))
    

if __name__ == "__main__":
    main()
    pass