#! /usr/bin/env python3
import os


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

        self.file_registery = {}


    def add_file(self, id:type, file_path:str, mode:str = "r"):
        """
        Adds a file to the internal registry.
        """

        if type(id) != self.expects_id_type:
            raise TypeError("Invalid identifer used for file object management.")

        file_object = File_Handler(file_path, mode)

        self.file_registery[id] = file_object


    def retrieve_file(self, id:type):
        """
        Retrieves a file from the registery.
        """

        if type(id) != self.expects_id_type:
            raise TypeError("Invalid identifier used for file object look up.")

        if self.file_registery.get(id) is None:
            return None
        
        return self.file_registery[id]


    def remove_file(self, id):
        """
        Removes a file from the interal registery.
        """

        if type(id) != self.expects_id_type:
            raise TypeError("Invalid identifier used for file object deletion")
        
        if self.file_registery.get(id) is None:
            return None
        
        self.file_registery.pop(id)


    def __del__(self):
        """
        We dereference the internal registery, triggering the file_handlers to close their files.
        """
        del self.file_registery


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


    def find_index(self):
        """
        Returns the current index of the file reader.

        ### Returns

        `int` - An integer representing the current position of the file.
        """
        return self.file_object.tell()


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
        if self.supports_read is not True:
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


    def write_file(self, content:str|bytes, flush:bool = True):
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
            raise InvalidFileOperation(f"InvalidFileOperation: File Mode {self.mode} does not support write.")
        
        # execute write
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
            self.__create_file(new_file_name)


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


    # private methods


    def __check_file_exists(self):
        """
        Private function that checks if a given file path exists.

        ### Raises

        `FileNotFoundError` - The file does not exist.

        ### Returns:

        `int` - An integer returncode of 0.
        """
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
            self.mode = "r"
            self.__create_file(self.file_location)
            return True, False

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
        self.file_object.flush()
        self.file_object.close()


def main():
    pass

if __name__ == "__main__":
    main()