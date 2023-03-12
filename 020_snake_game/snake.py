import turtle as t
import random as r
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0
INITIAL_POSITION = [(-10, 10), (-30, 10), (-50, 10)]


class Snake:
    def __init__(self, ):
        """Initializing variables"""
        self.snake = []
        self.snake_parked = []
        self.create_initial_snake()
        self.head = self.snake[0]

    def create_initial_snake(self):
        """Creates the starting snake"""
        for n in range(3):
            self.add_snake_block(INITIAL_POSITION[n])

    def add_snake_block(self, pos):
        """Create a snake block and assign the position with pos"""
        if len(self.snake_parked):
            tmp = self.snake_parked.pop()
        else:
            tmp = t.Turtle('square')
            tmp.color('#' + ''.join(r.choices('0123456789ABCDEF', k=6)))
            tmp.up()
        tmp.setpos(pos)
        self.snake.append(tmp)

    def move(self):
        """Moves the snake forward"""
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i].setpos(self.snake[i - 1].pos())
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        """Moves the snake up"""
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        """Moves the snake down"""
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        """Moves the snake left"""
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        """Moves the snake right"""
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    def extend_snake(self):
        self.add_snake_block(self.snake[-1].pos())

    def reset(self):
        for s in self.snake[3:]:
            s.setpos(-800, -800)
            self.snake_parked.append(s)
            self.snake.remove(s)

        self.head.setheading(RIGHT)
        for n, s in enumerate(self.snake):
            s.setpos(INITIAL_POSITION[n])
