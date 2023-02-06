import sys,os
import curses

def draw_menu(stdscr):
    curses.curs_set(0)
    k = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()
    stdscr.nodelay(True)

    # Start colors in curses
    curses.start_color()
    # curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    # curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    # curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    contents = []
    # Loop where k is the last character pressed
    while True:
        # get the key input
        k = stdscr.getch()
        match k:
            case -1:
                continue
            case 4:
                break
            case curses.KEY_BACKSPACE:
                contents = contents[0:-1]

        char = chr(k)
        if k not in (curses.KEY_DOWN, curses.KEY_UP, curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_BACKSPACE):
            contents.append(char)

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Declaration of strings
        keystr = "Last key pressed: {}".format("".join(contents))[:width-1]
        statusbarstr = "Press 'CTRL+D' to exit"

        # Centering calculations
        start_x_keystr = 0
        start_y = height


        # Render status bar
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))

        # Print rest of text
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)

        # Refresh the screen
        stdscr.refresh()

# def main():
#     curses.wrapper(draw_menu)

import curses
from textpad import rectangle, Textbox

def email_editor():
    # try for error catching and returning terminal to defaults
    try:
        # creating a mainwindow for the header message
        mainwindow = curses.initscr()
        
        # coloring window 
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        mainwindow.bkgd(" ", curses.color_pair(1) |curses.A_BOLD)
        # getting max x/y for centering math
        y, x = mainwindow.getmaxyx()
        
        # telling user what to do
        boot_message = "EMAIL MESSAGE SYSTEM BOOTED."
        subtext = "Please enter your message here. Enter Ctrl+D to save it."
        mainwindow.addstr(0, (x-len(boot_message))//2, boot_message)
        mainwindow.addstr(1, (x-len(subtext))//2, subtext)

        # refreshing window
        mainwindow.refresh()
        # echo off to stop keys entered from appearing twice
        curses.noecho()

        # creating a subwindow for the textbox
        editwin = curses.newwin(y,x, 3,0)
        i = Textbox(editwin)
        # allow user to edit.
        i.edit()

        # get message.
        message = i.gather()

    # finally means it always runs.
    finally:

        # shutdown windows
        curses.endwin()

    # return message
    return message
