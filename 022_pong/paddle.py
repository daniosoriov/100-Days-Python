import turtle as t
MOVEMENT = 30


class Paddle(t.Turtle):

    def __init__(self, position):
        """The position on the canvas"""
        super().__init__()
        self.shape('square')
        self.color('white')
        self.shapesize(stretch_len=1, stretch_wid=5)
        self.up()
        self.hideturtle()
        self.setpos(position)
        self.showturtle()

    def move_up(self):
        """Moves the paddle up"""
        newx = self.ycor() + MOVEMENT
        if newx > 280:
            newx = 260
        self.setpos(self.xcor(), newx)

    def move_down(self):
        """Moves the paddle down"""
        newx = self.ycor() - MOVEMENT
        if newx < -250:
            newx = -245
        self.setpos(self.xcor(), newx)

    def computer_move(self, posy):
        """Moves the computer based on the y position of the ball"""
        self.setpos(self.xcor(), posy)
