import turtle as t
FONT = ('Arial', 40, 'normal')
FONT_MESSAGE = ('Arial', 20, 'normal')
SCORE_POS = (0, 200)


class ScoreBoard(t.Turtle):

    def __init__(self):
        super().__init__()
        self.color('white')
        self.up()
        self.hideturtle()
        self.left_score = 0
        self.right_score = 0
        self.setpos(SCORE_POS)
        self.update_score()

    def update_score(self):
        """Updates the score at the top of the screen"""
        self.setpos(SCORE_POS)
        self.clear()
        self.write(arg=f'{self.left_score} - {self.right_score}', move=False, align='center', font=FONT)

    def left_point(self):
        """Gives an extra point to the left paddle"""
        self.left_score += 1
        self.update_score()

    def right_point(self):
        """Gives an extra point to the right paddle"""
        self.right_score += 1
        self.update_score()

    def new_round(self):
        """Announcing a new round"""
        self.setpos(0, 0)
        self.write(arg='New round', move=False, align='center', font=FONT_MESSAGE)

    def game_over(self):
        """Announcing that the game is over"""
        self.setpos(0, 0)
        self.write(arg='Game over!', move=False, align='center', font=FONT_MESSAGE)
