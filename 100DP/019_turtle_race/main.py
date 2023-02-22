import turtle as t
import random as r

screen = t.Screen()
screen.setup(width=500, height=400)
color = screen.textinput(title='Choose a color', prompt='Choose a color between red, orange, yellow, green, '
                                                        'blue or purple').lower().strip()

colors = ('red', 'orange', 'yellow', 'green', 'blue', 'purple')
turtles = []
for n, c in enumerate(colors):
    tmp = t.Turtle(shape='turtle')
    tmp.color(c)
    tmp.up()
    tmp.setpos(x=-230, y=-140 + 40 * (n + 1))
    turtles.append(tmp)

if color:
    carry_on = True
    while carry_on:
        tmp = r.choice(turtles)
        tmp.forward(r.randint(5, 25))
        if tmp.xcor() > 230:
            carry_on = False
            winner_color = tmp.pencolor()
            comparison = f'The winner is {winner_color} and your choice was {color}.'
            if color == winner_color:
                print(f'You won! {comparison}')
            else:
                print(f'You lost! {comparison}')

screen.exitonclick()
