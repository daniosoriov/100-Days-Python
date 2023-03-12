"""Functionality for the runner turtle"""
import turtle as t
SPEED = 10


class Runner(t.Turtle):

    def __init__(self, position):
        super().__init__()
        self.up()
        self.initial_position = position
        self.setpos(position)
        self.setheading(90)
        self.shapesize(stretch_len=1.5, stretch_wid=1.5)
        self.color('black')
        self.shape('turtle')

    def move_up(self):
        """Moves the turtle up"""
        self.forward(SPEED)

    def move_down(self):
        """Moves the turtle down"""
        if self.ycor() + SPEED > -260:
            self.backward(SPEED)

    def new_level(self):
        """Resets the turtle to its initial position"""
        self.setpos(self.initial_position)
