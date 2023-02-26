"""A simple Pong game for two players"""
import turtle as t
import ball
import paddle
import scoreboard

screen = t.Screen()
screen.setup(width=800, height=600)
screen.bgcolor('black')
screen.title('Pong!')
screen.tracer(0)

ball = ball.Ball()
right_paddle = paddle.Paddle((360, 0))
left_paddle = paddle.Paddle((-370, 0))
scoreboard = scoreboard.ScoreBoard()
screen.update()

screen.listen()
screen.onkeypress(fun=right_paddle.move_up, key='Up')
screen.onkeypress(fun=right_paddle.move_down, key='Down')
screen.onkeypress(fun=left_paddle.move_up, key='w')
screen.onkeypress(fun=left_paddle.move_down, key='s')

# Only allow 10 games
games = 0
while games < 10:
    screen.update()
    ball.move()

    # Check if the ball bounces
    if ball.ycor() > 286 or ball.ycor() < -278:
        ball.bounce()

    # Check if it hits a paddle
    if ball.distance(left_paddle.pos()) < 50 and ball.xcor() < -350 or ball.distance(
            right_paddle.pos()) < 50 and ball.xcor() > 340:
        ball.hit_paddle()

    # Left paddle scores
    if ball.xcor() > 378:
        scoreboard.left_point()
        games += 1
        ball.restart()

    # Right paddle scores
    if ball.xcor() < -387:
        scoreboard.right_point()
        games += 1
        ball.restart()

scoreboard.game_over()

screen.exitonclick()
