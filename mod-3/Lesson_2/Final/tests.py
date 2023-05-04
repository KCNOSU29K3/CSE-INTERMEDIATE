#! /usr/bin/env python3
import pytest

"""
Testing file. Ran with pytest.
"""


import os
from main import File_Handler, File_Manager, Inventory_Manager


test_file_name = "./TEST_FILE.txt"
test_file_two = "./TEST_FILE_2.txt"



class TestClass_File_Handler:
    """
    Testing class for the `File_Handler` class.
    """


    def test_file_creation_ops(self):
        """
        Tests File Creation capabilities.
        """
        auto_file_opener_ops = ["w", "w+", "wb", "wb+", "x"]
        for op in auto_file_opener_ops:
            if os.path.exists(test_file_name):
                os.remove(test_file_name)
            File_Handler(test_file_name, op)
            assert os.path.exists(test_file_name) == True, f"File creation with {op} operator failed"


    def test_file_write(self):
        """
        Tests file handler write capabilities
        this also tests read capabilities of + operators
        """
        write_capable_ops = ["a", "w", "ab", "wb", "a+", "w+", "ab+", "wb+"]
        for op in write_capable_ops:
            if not os.path.exists(test_file_name):
                File_Handler(test_file_name, "x")
            file_handler = File_Handler(test_file_name, op)
            file_handler.write_file("Hello")
            file_handler.goto(0)
            if "+" not in op:
                del file_handler
                file_handler = File_Handler(test_file_name, "rb" if "b" in op else "r")
            if "b" in op:
                assert file_handler.read_file() == b"Hello", "Read/write discrepancy with {} operator.".format(op)
            else:
                assert file_handler.read_file() == "Hello", "Write/read discrepancy with {} operator.".format(op)
            os.remove(test_file_name)


    def test_x_op(self):
        """
        Ensures that implementation of the `'x'` operator
        is functioning as intended.
        """
        if os.path.exists(test_file_name):
            os.remove(test_file_name)
        x = File_Handler(test_file_name, "x")
        del x
        assert os.path.exists(test_file_name) == True, "File not created when expected to."

        # this should raise a FileNotFoundError
        with pytest.raises(FileExistsError):
            x = File_Handler(test_file_name, "x")
            del x

        os.remove(test_file_name)


    def test_file_read(self):
        """
        Tests that read-only operators are functional.
        """
        if not os.path.exists(test_file_name):
            tmp = File_Handler(test_file_name, "w")
            tmp.write_file("Hello")
            del tmp

        file_handler = File_Handler(test_file_name, "r")
        assert file_handler.read_file() == "Hello", "File read discrepancy."
        del file_handler

        file_handler = File_Handler(test_file_name, "rb")
        assert file_handler.read_file() == b"Hello", "File bytes read discrepancy."
        del file_handler

        os.remove(test_file_name)
        pass


    def test_write_to_read_change(self):

        write_operators = ["w", "wb", "a", "ab"]
        read_operators = ["r", "rb"]

        for op in write_operators:
            if os.path.exists(test_file_name):
                os.remove(test_file_name)
            File_Handler(test_file_name, "x")

            file_handler = File_Handler(test_file_name, op)
            file_handler.write_file("Hello")
            file_handler.change_file_mode("r")

            assert file_handler.read_file() == "Hello", "Read discrepancy after changing modes."
            file_handler.change_file_mode("rb")
            assert file_handler.read_file() == b"Hello", "Read Discrepancy after changing modes"
        os.remove(test_file_name)


    def test_read_to_write_change(self):
        # test setup
        def setup():
            tmp = File_Handler(test_file_name, "w")
            tmp.write_file("Hello, World!")

        def teardown():
            os.remove(test_file_name)

        read_operators = ["r", "rb"]
        for op in read_operators:
            setup()
            file_handler = File_Handler(test_file_name, op)
            content_before_write = file_handler.read_file()

            file_handler.change_file_mode("a")
            file_handler.write_file("Changing contents...")
            file_handler.change_file_mode("r")
            assert file_handler.read_file() != content_before_write
            teardown()


    def test_file_change(self):
        """
        Tests that file writing/reading functions correctly between 
        file switches.
        """

        file_handler = File_Handler(test_file_name, "w")
        file_handler.write_file("Hello, World!")
        file_handler.change_file_name(test_file_two)

        file_handler.write_file("Hello, World!")
        file_handler.change_file_mode("r")

        content_2 = file_handler.read_file()
        file_handler.change_file_name(test_file_name)
        content = file_handler.read_file()

        assert content == content_2, "Discrepancy after changing file write."

        os.remove(test_file_name)
        os.remove(test_file_two)


    def test_readlines(self):
        """
        tests that readlines functions as intended.
        Also tests that writelines functions.
        """
        data = ["Hello\n", "World!"]

        file_handler = File_Handler(test_file_name, "w")
        file_handler.write_file(data, True, True)
        file_handler.change_file_mode("r")

        return_lines = file_handler.read_file(0, True)
        assert data == return_lines, "Readlines discrepancy detected."
        
        pass


    def test_cleanup(self):
        """
        Cleans up resultant test files.
        """
        if os.path.exists(test_file_name):
            os.remove(test_file_name)
        elif os.path.exists(test_file_two):
            os.remove(test_file_two)