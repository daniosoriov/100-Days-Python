import turtle as t
import time
import snake
import food
import scoreboard

screen = t.Screen()
screen.setup(width=600, height=600)
screen.bgcolor('black')
screen.title('Snake game')
screen.tracer(0)

snake = snake.Snake()
food = food.Food()
scoreboard = scoreboard.Scoreboard()
screen.listen()

screen.onkeypress(fun=snake.up, key='Up')
screen.onkeypress(fun=snake.down, key='Down')
screen.onkeypress(fun=snake.left, key='Left')
screen.onkeypress(fun=snake.right, key='Right')

play = True
while play:
    screen.update()
    time.sleep(0.1)

    snake.move()
    # If it collides with the food.
    if (snake.head.distance(food)) < 15:
        snake.extend_snake()
        food.new_position()
        scoreboard.increase()

    # Crashed against wall
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
        scoreboard.game_over('You crashed against the wall!')
        play = False

    # Crashed against itself
    for block in snake.snake[1:]:
        if snake.head.distance(block) < 10:
            scoreboard.game_over('You crashed against yourself!')
            play = False

screen.exitonclick()
