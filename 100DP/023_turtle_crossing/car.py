"""Handles the functionality of each car"""
import turtle as t
import random as r


class Car(t.Turtle):

    def __init__(self, position):
        super().__init__()
        self.up()
        self.color('#' + ''.join(r.choices('123456789ABCDEF', k=6)))
        self.shape('square')
        self.setheading(180)
        self.shapesize(stretch_wid=1.5, stretch_len=2)
        self.setpos(position)

    def move(self):
        """Gets a car to move"""
        self.setpos(self.xcor() - 10, self.ycor())

    def park_car(self, position):
        self.setpos(position)
