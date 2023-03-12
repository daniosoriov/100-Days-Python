import turtle as t
import random as r
BALLSPEED = 3


class Ball(t.Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.up()
        self.shape('circle')
        self.color('white')
        self.showturtle()
        self.dirx = BALLSPEED * r.choice((-1, 1))
        self.diry = BALLSPEED * r.choice((-1, 1))
        self.restart()

    def restart(self):
        """It restarts the ball to go the opposite direction"""
        self.home()
        current_x = self.dirx
        self.dirx = BALLSPEED
        if current_x > 0:
            self.dirx *= -1
        self.diry *= r.choice((-1, 1))

    def move(self):
        """Moves the ball"""
        self.setpos(self.xcor() + self.dirx, self.ycor() + self.diry)

    def bounce(self):
        """Bounces the ball off the north and south walls"""
        self.diry *= -1

    def hit_paddle(self):
        """Bounces the ball off the paddle and increases speed"""
        self.dirx *= -1.1
