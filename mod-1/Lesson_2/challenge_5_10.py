import math
from turtle import Turtle, Screen, left


def get_screen():
    """
    Returns a Screen object.
    """
    screen = Screen()
    return screen


def draw_n_side_shape(num_sides:int, side_length:int, start_angle:int, center_on:tuple, color, infill=True, pensize=5):
    """
    A function that draws a shape with `n` sides to an existing Screen.
    ### Parameters
    `num_sides` : The number of sides the shape should have.
    `side_length` : How long the sides of the shape should be.
    `start_angle` : what angle to tilt the shape at. Rotates left.
    `center_on` : The x/y coordinates of the point to start at.
    `color` : the color and infill color of the shape, if applicable.
    `infill` : parameter that toggles infilling of shapes.
    `pensize` : The size of the pen to draw with.
    """
    # calculating angle
    angle = 360/num_sides
    # setting turtle + attributes
    turt = Turtle()
    turt.hideturtle()
    turt.speed(0)
    turt.pensize(pensize)
    turt.color(color)
    turt.penup()
    turt.goto(center_on)
    # turt.left(angle)
    turt.left(start_angle)
    turt.pendown()


    # drawing shape
    if infill is True:
        turt.fillcolor(color)
        turt.begin_fill()
        for i in range(num_sides):
            turt.forward(side_length)
            turt.left(angle)
        turt.end_fill()
    else:
        for i in range(num_sides):
            turt.forward(side_length)
            turt.left(angle)
    del turt


def draw_spiral(angle:int, start_size:int, pensize:int, color:str, center_on:tuple[int, int], iterations:int, increase_by:int):
    """
    Creates a square spiral. 

    ### Parameters

    `angle` The angle to turn when finishing a spiral line.

    `start_size` The amount of pixels to go forward when starting.

    `pensize` The size of the pen when drawing.

    `color` A color name or hex string indicating the color to make the spiral.

    `center_on` The coordinates to begin creating the spiral

    `iterations` How many times the function should create a spiral side.

    `increase_by` The size to increase each side by.

    ### Returns

    Nothing. 
    """
    # setting turtle + attributes
    turt = Turtle()
    turt.hideturtle()
    turt.speed(0)
    turt.pensize(pensize)
    turt.color(color)
    turt.penup()
    turt.goto(center_on)
    turt.pendown()

    for i in range(iterations):
        turt.forward(start_size)
        start_size += increase_by
        turt.left(angle)


def draw_sprite(num_legs, length, pensize, color, start_at):
    angle = 360/num_legs


    turt = Turtle()
    turt.penup()
    turt.hideturtle()
    turt.speed(0)
    turt.goto(start_at)
    turt.pensize(pensize)
    turt.color(color)
    turt.pendown()
    for i in range(num_legs):
        turt.forward(length)
        turt.back(length)
        turt.left(angle)



if __name__ == "__main__":

    i = int(input("Enter a challenge number from 5 - 10 \n"))
    screen = get_screen()

    # ignore this godforsaken conditional tree
    if i == 6:
        size = 20
        x = 0
        y = 0

        # squares in squares
        for i in range(20):
            draw_n_side_shape(4, size, 0, (x, y), "red", False)
            size += 20
            x -= 10
            y -= 10
        input("Press enter to continue")


    elif i == 5:
        x = -50
        for i in range(5):
            draw_n_side_shape(4, 20, 0, (x, 0), 'red', False, 1)
            x += 40
        input("Press enter to continue")


    elif i == 7:
        draw_n_side_shape(8, 50, 0, (0,0), "red", False, 1)
        input("Press enter to continue")


    elif i == 9:
        # spiral 1
        draw_spiral(89, 5, 2, "red", (0, 0), 100, 5)
        input("enter to continue")

        screen.clear()

        # spiral 2
        draw_spiral(90, 5, 3, "red", (0, 0), 100, 5)
        input("enter to continue")


    elif i == 10:
        draw_sprite(15, 120, 5, "red", (0,0))
        input("enter to continue")


    elif i == 8:
        angle = 0
        for i in range(36):
            draw_n_side_shape(4, 100, angle, (0, 0), "red", False, 1)
            angle += 10
        input("Press enter to continue")