import turtle as t
import random as r
POSITIONS = range(-280, 280, 10)


class Food(t.Turtle):

    # TODO: make that the food is always centered aligned with the snake, so it has to be multiple of 20, I think
    # TODO: food shouldn't appear where the snake body currently is, so random is ok, but not as the snake grows.
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.up()
        self.shapesize(stretch_len=0.75, stretch_wid=0.75)
        self.color('red')
        self.speed(0)
        self.setpos(x=r.choice(POSITIONS), y=r.choice(POSITIONS))

    def new_position(self):
        self.setpos(r.choice(POSITIONS), r.choice(POSITIONS))
