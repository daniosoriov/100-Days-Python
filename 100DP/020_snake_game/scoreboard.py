import turtle as t
FONT = ('Arial', 18, 'normal')


class Scoreboard(t.Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.color('white')
        self.up()
        self.hideturtle()
        self.update_score()

    def game_over(self, message=''):
        self.setpos(-20, -40)
        self.write(arg=f'Game over! {message}', move=False, align='center', font=FONT)

    def increase(self):
        self.score += 1
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(arg=f'Score: {self.score}', move=False, align='center', font=FONT)
