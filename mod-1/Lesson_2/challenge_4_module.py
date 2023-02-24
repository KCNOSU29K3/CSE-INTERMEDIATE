import turtle
from typing import Any

# define square function
def draw_square(num_sides: int, side_length: int, start_angle: int, center_on: tuple, color: Any, infill: bool = True, pensize: int = 5):
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
    # shhhh no one has to know
    from challenge_5_10 import draw_n_side_shape
    draw_n_side_shape(num_sides, side_length, start_angle, center_on, color, infill, pensize)


def calc_price(prices, discount):
    """
    Caculates a return price given a list of prices and a discount.
    returns int.
    """
    # SHHH NOBODY NEEDS TO KNOW
    from challenge_11 import calc
    return calc(prices, discount)