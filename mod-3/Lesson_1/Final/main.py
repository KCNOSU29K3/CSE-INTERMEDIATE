#! /usr/bin/env python3

# imports

import os
from turtle import Turtle, Screen

# for future compatability updates 
from pathlib import Path 


import logging
import zipfile
from base64 import decodebytes
from time import perf_counter


if not os.path.exists(".logs.log"):
    with open (".logs.log", "x") as file:
        pass


# constant data and setup

color_name_to_RGB = {
"red" : (255, 0, 0),
"green" : (0, 255, 0), 
"blue" : (0, 0, 255),
"grey" : (102, 153, 204),
"yellow" : (255, 255, 0),
"orange" : (255, 165, 0),
"indigo" : (73, 0, 130),
"violet" : (143, 0, 255), 
"black" : (0, 0, 0),
"magenta" : (255, 0, 255),
"white" : (255, 255, 255),
"cyan" : (100, 0, 100),
"purple" : (160, 32, 240),
"silver" : (192, 192, 192),
"pink" : (255, 192, 203),
"maroon" : (128, 0, 0),
"brown" : (150, 75, 0),
"beige" : (245, 245, 220),
"tan" : (210, 180, 140),
"peach" : (255, 229, 180),
"lime" : (50, 205, 50),
"olive" : (128, 128, 0),
"turquoise" : (48, 213, 200),
"teal" : (0, 128, 128),
"navy blue" : (0, 0, 128)
}


file_data = [
b"""
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

"""
]


def clear():
    """
    Basic function that clears the screen
    """
    os.system("cls" if os.name == "nt" else "clear")
    return 0


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


class Turtle_Drawing:
    """
    A class used to execute the drawing commands needed for 
    this project.
    """


    def __init__(self, speed:int = 0) -> None:
        

        # drawing variables
        self.screen = Screen()
        self.turtle = Turtle()


        # turtle config
        self.turtle.speed(speed)
        self.turtle.hideturtle()


        self.title = None
        pass


    def parse_data(self, lines:list[str]):
        for line in lines:
            line = line.replace("\n", "")
            # print(f"LINE IS '{line}'")
            match line:
                case "UP":
                    self.turtle.penup()
                case "DOWN":
                    self.turtle.pendown()
                case _:
                    if "NAME" in line:
                        self.title = line.split(":")[1]
                        continue
                    elif "BACKGROUND" in line:
                        self.screen.bgcolor(line.split(":")[1])
                        continue
                    elif "PENCOLOR" in line:
                        self.turtle.pencolor(line.split(":")[1])
                        continue
                    x_coord, y_coord = line.split(" ")
                    self.__exec_instruction(x_coord, y_coord)


    def __exec_instruction(self, x_coord, y_coord):
        
        self.turtle.goto(float(x_coord), float(y_coord))


    def finalize(self):
        """
        Finalizes the drawing by adding a title and waiting for click to 
        exit.

        ### Returns

        `int` - An integer returncode of 0.
        """
        self.turtle.penup()
        self.turtle.goto(200, 0)
        self.turtle.pendown()
        self.turtle.write(self.title if self.title != "" else "Dinosaur", font=("Arial", 20, "bold"))
        self.__hold_until_click()


    def clear_screen(self):
        """
        Clears all drawings on the screen.

        ### Returns

        `int` - An integer returncode of 0.
        """
        self.turtle.clear()
        return 0



    def ask_for_input(self, title:str = "default", prompt:str = "default"):
        """
        Prompts the screen for a text input.

        ### Parameters

        `title` : The title of the prompt window.

        `prompt` : The prompt for the prompt window.

        ### Returns

        `str` - The result from the prompt.

        `None` - The Window was closed.
        """
        return self.screen.textinput(title, prompt)


    def __hold_until_click(self):
        """
        Private function that stops the turtle window from exiting.
        """
        self.screen.exitonclick()


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
    """
    Main function.
    """

    # generate data if not found
    if not os.path.exists("./external_turtle_file_windows.txt"):
        generate_data_if_not_existent()


    # instantiate with known existent file.
    system_file_handler = File_Handler("./external_turtle_file_windows.txt")
    system_file_handler.set_encoding("utf-16")

    lines = system_file_handler.read_file(return_lines=True)

    # draw picture
    drawer = Turtle_Drawing()
    drawer.parse_data(lines)

    # query for data
    name = drawer.ask_for_input("Title of Work", "Please enter the name you wish to title this work:")
    background_color = drawer.ask_for_input("Background color", "Please enter the desired background color:").lower()
    drawing_color = drawer.ask_for_input("Pen Color", "Please enter the desired pen color:").lower()

    # ensure colors exist
    if color_name_to_RGB.get(background_color) is None:
        
        print("Color not supported. Defaulting to white background.")
        background_color = "white"

    if color_name_to_RGB.get(drawing_color) is None:

        drawing_color = "black"
        print("Color not supported. Defaulting to black pen color.")

    name = name if name != "" else "default"

    # create new file, or if file exists overwrite current data
    
    system_file_handler.change_file_name(f"./{name}.txt", True)
    system_file_handler.change_file_mode("w+")

    # write new data
    system_file_handler.write_file(f"NAME:{name}\n")
    system_file_handler.write_file(f"BACKGROUND:{background_color}\n")
    system_file_handler.write_file(f"PENCOLOR:{drawing_color}\n")

    # write old data
    for line in lines:
        system_file_handler.write_file(line)

    # read file
    lines = system_file_handler.read_file(return_lines=True, index=0)

    # draw
    drawer.clear_screen()
    drawer.parse_data(lines)
    drawer.finalize()









if __name__ == "__main__":
    main() 