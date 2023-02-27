"""Main file of the turtle crossing game"""
import turtle as t
import time
import game
import runner
import scoreboard

screen = t.Screen()
screen.setup(width=600, height=600)
screen.title('Turtle crossing!')
screen.tracer(0)

scoreboard = scoreboard.ScoreBoard()
game = game.Game()

run = runner.Runner((0, -260))
screen.listen()
screen.onkeypress(fun=run.move_up, key='Up')
screen.onkeypress(fun=run.move_down, key='Down')

iterations = 0
scoreboard.update_score()
game_on = True
while game_on:
    screen.update()
    # Reduce the time on each level
    time.sleep(game.time)

    # Launch a new car every X iterations, the iterations are faster as we increase levels
    if iterations % game.iterations == 0:
        game.start_car()

    # Make all the moving cars move accross the screen
    for car in game.cars_moving:
        car.move()
        # If a car collides with the turtle, stop the game
        if run.distance(car.pos()) < 30:
            game_on = False
            scoreboard.game_over()
            break

        # If a car reaches the end, park it, so we can reuse it later
        if car.xcor() < -400:
            game.park_car(car)

    # The runner reached the end of the screen, move on to the next level
    if run.ycor() > 270:
        scoreboard.update_score()
        game.next_level()
        run.new_level()
        time.sleep(1)
        iterations = -1

    iterations += 1

screen.exitonclick()
