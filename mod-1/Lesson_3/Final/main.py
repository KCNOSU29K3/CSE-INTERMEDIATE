#!/usr/bin/env python3


import random
from time import perf_counter_ns
from turtle import Turtle, Screen


def timed(function):
    """
    Returns the value of a function and the time it took to run in nanoseconds.
    """
    

    def wrapper(*args, **kwargs):
        # grabs the performance time in NS

        start = perf_counter_ns()
        i = function(*args, **kwargs)
        end = perf_counter_ns()
        ns = end - start
        s = ns/1000000000
        return i, ns, s

    return wrapper


class TurtleLogic:
    """
    Class that governs underlying turtle logic.

    ### Parameters

    `turt_names` - The names of the two turtles stored in a tuple.

    `turt_colors` - The colors of the two turtles stored in a tuple.

    `speed` - An integer representing the desired speed of the turtle (0 is fastest).
    """
    

    def __init__(self, turt_names:tuple[str, str], turt_colors:tuple[str, str], speed:int) -> None:

        self.screen = Screen()
        # define turtles
        # turts are zero-indexed to match Python Syntax
        self.turt_0 = Turtle()
        self.turt_1 = Turtle()
        self.turt_ref = Turtle()

        # give them names
        # this works because we are just tacking on a variable to the class instance
        self.turt_0.name = turt_names[0]
        self.turt_1.name = turt_names[1]
        self.turt_ref.name = "Referee"

        # give them colors
        self.turt_0.color(turt_colors[0])
        self.turt_1.color(turt_colors[1])
        self.turt_ref.color("black")

        # set the speed
        self.turt_0.speed(speed)
        self.turt_1.speed(speed)


    def draw_field(self, length:int, width:int) -> None:
        """
        Draws a field of a given `length` and `width` onto the screen.

        ### Parameters

        `length` - The required length of the field as an integer.

        `width` - The required width of the field as an integer. 

        ### Returns

        `None`.
        """

        # setting the field boundaries
        # little known fact about turtles:
        # when you draw 2 units to the screen with a turtle, it
        # only moves the turtle 1 positional unit.
        self.max_x = length//2
        self.max_y = width//2

        # get to the correct area
        self.turt_ref.penup()
        self.turt_ref.speed(0)
        self.turt_ref.pensize(10)
        self.turt_ref.forward(length//2)
        self.turt_ref.left(90)
        self.turt_ref.pendown()

        # draw square
        self.turt_ref.back(width//2)
        self.turt_ref.forward(width)
        self.turt_ref.left(90)
        self.turt_ref.forward(length)
        self.turt_ref.left(90)
        self.turt_ref.forward(width)
        self.turt_ref.left(90)
        self.turt_ref.forward(length)

        # put ref at visually pleasing pos
        self.turt_ref.penup()
        self.turt_ref.goto(0, 0)
        self.turt_ref.left(90)
        self.turt_ref.forward(width//2 + 20)
        self.turt_ref.left(180)


    def run_turtles(self) -> str:
        """
        Runs the turtle game. Will return the name of the winner.

        Takes no parameters.
        """
        
        # event loop
        while True:
            
            # get turning angles
            turn_angle_0 = random.choice(range(361))
            turn_angle_1 = random.choice(range(361))

            # do turtle 0 first

            self.turt_0.left(turn_angle_0)
            self.turt_0.forward(50)

            turt_0_x, turt_0_y = self.turt_0.pos()


            # check if out of bounds
            if turt_0_x > self.max_x or turt_0_y > self.max_y:
                return self.turt_1.name
            
            elif turt_0_x < -self.max_x or turt_0_y < -self.max_y:
                return self.turt_1.name
            
            # turtle 1
            self.turt_1.left(turn_angle_1)
            self.turt_1.forward(50)

            turt_1_x, turt_1_y = self.turt_1.pos()

            # check if out of bounds
            if turt_1_x > self.max_x or turt_1_y > self.max_y:
                return self.turt_0.name
            
            if turt_1_x < -self.max_x or turt_1_y < -self.max_y:
                return self.turt_0.name


    def run_gui(self) -> None:
        """
        Runs the GUI. Takes no parameters and returns None.
        """

        # get our winner
        winner = self.run_turtles()

        # write out winner to screen
        self.turt_ref.write(f"The Winner is: {winner}", align="Center", font=("Arial", 50, "bold"))
        
        # get out of way
        self.turt_ref.back(60)

        # wait for user to click.
        self.screen.exitonclick()


class CLI_Interface(TurtleLogic):


    def __init__(self) -> None:

        # get data from user

        turtle_0_name = input("What is the name of the first turtle?\n")
        turtle_1_name = input("What is the name of the second turtle?\n")
        turtle_0_color = input("What is the color of the first turtle?\n")
        turtle_1_color = input("What is the color of the second turtle?\n")
        turtle_speed = int(input("What should the speed of the turtles be? (0 is fastest)\n"))

        length = float(input("What should the length of the arena be?\n"))
        width = float(input("What should the width of the arena be?\n"))


        # inherit and run
        super().__init__((turtle_0_name, turtle_1_name), (turtle_0_color, turtle_1_color), turtle_speed)
        self.draw_field(length, width)
        self.run_gui()


# get performance characteristics.
@timed
def main():
    """
    Main Function.
    """
    try:
        CLI_Interface()
    
    except ValueError:
        print("Unusable value entered\nIrrecoverable: Exiting with code -1")
        exit(-1)
    
    except Exception as E:
        print("Unknown Error detected: {E}\nIrrecoverable: Exiting with code -999")
        exit(-999)


if __name__ == "__main__":
    null, ns, s = main()
    print(f"Program ran in {ns} nanoseconds | {s} seconds.")