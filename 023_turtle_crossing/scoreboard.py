"""Updates the score and announces when the game is over"""
import turtle as t
FONT = ('Arial', 20, 'normal')


class ScoreBoard(t.Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.up()
        self.setpos(0, 260)
        self.level = 0

    def update_score(self):
        """Update the score"""
        self.level += 1
        self.clear()
        self.write(arg=f'Level {self.level}', move=False, align='center', font=FONT)

    def game_over(self):
        """Game over"""
        self.setpos(0, 0)
        self.write(arg='Game over!', move=False, align='center', font=FONT)
