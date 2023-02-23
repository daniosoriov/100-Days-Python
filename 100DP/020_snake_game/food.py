import turtle as t
import random as r


class Food(t.Turtle):

    # TODO: make that the food is always centered aligned with the snake, so it has to be multiple of 20, I think
    # TODO: make the food a bit bigger
    # TODO: food shouldn't appear where the snake body currently is, so random is ok, but not as the snake grows.
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.up()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color('red')
        self.speed(0)
        self.setpos(x=r.randint(-280, 280), y=r.randint(-280, 280))

    def new_position(self):
        self.setpos(x=r.randint(-280, 280), y=r.randint(-280, 280))
