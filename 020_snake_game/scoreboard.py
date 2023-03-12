import turtle as t
FONT = ('Arial', 18, 'normal')


class Scoreboard(t.Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        try:
            with open('score.txt') as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0
        self.color('white')
        self.up()
        self.hideturtle()
        self.update_score()

    def game_over(self, message=''):
        self.setpos(-20, -40)
        self.write(arg=f'Game over! {message}', move=False, align='center', font=FONT)

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open('score.txt', 'w') as file:
                file.write(str(self.high_score))
        self.score = 0
        self.update_score()

    def increase(self):
        self.score += 1
        self.update_score()

    def update_score(self):
        self.clear()
        self.home()
        self.write(arg=f'Score: {self.score} - High score: {self.high_score}', move=False, align='center', font=FONT)
