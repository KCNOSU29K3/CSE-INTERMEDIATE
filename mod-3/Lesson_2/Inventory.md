# Inventory

## Problem

    A company needs a program that allows for the setting of base stock, the ability to restock, and the ability to make purchases, in that order. 3 files, the base stock, restock, and purchases, must be able to be output to `stdout` at the end of the program. 

    The base stock file must contain all offered stock with a stock amount of 0.
    The restock file must contain an updated stock with given restock amounts.
    The purchases file must contain the updated stock with purchased stock deleted.

    All files will be encoded in JSON.

## Program Flow

### File Management

  A `File_Manager` class will be used to wrap `File_Handler` objects and handle the code needed to interface with multiple files at once. It will be used to open and write to all files.

### Inventory Management

  An `Inventory_Manager` class will be used to effect changes on the internal inventory. This will be done to prevent unnecessary reads from files.

### Miscellaneous

  Several miscellaneous functions will be needed for niche applications. They are listed as follows

  1. String parsers. These functions will be used to parse input and ensure that it is usable. They will also be used to ensure that a given string can be converted to a given type.

  2. `stdout` functions. These functions will primarily be used to clear the `stdout` so as to prevent UI clutter.

  3. System functions. These will be used to restart the program if an unknown error occurred, or if a restart is the most efficient way to re-do something.

## Processing

### Base Stock

  The user will be prompted to enter the names of items and prices. The user will have the opportunity to validate these inputs and they will be parsed. If a discrepancy is detected, the program will restart. The data will then be output through the `File_Manager` and `Inventory_Manager`.

### Restock

  The user will be prompted to enter a system ID that describes a given stock item, through an input loop. They will then be asked to provide a number to restock it by. If a discrepancy is detected, the user will be informed and then the input loop will continue. Upon providing a breakout input, the loop will be broken and the data will be output through the `File_Manager` and the inventory will be updated through the `Inventory_Manager`.

### Purchase

  The user will be prompted to provide a system ID representing a stock item and then an amount to purchase through an input loop. If a discrepancy is detected, the loop will continue. Upon providing a breakout input, the loop will be broken and the data will be output through the `File_Manager`. The resultant money accrued from purchases will be returned.

### End

  The user will be prompted to decide which file they want to view. A match statement will call the output function which will print out the data.
