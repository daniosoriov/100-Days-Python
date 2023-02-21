import turtle as t
import random as r
import colorgram as c

extracted_colors = c.extract('image.jpg', 50)
colors = []
for color in extracted_colors:
    if color.rgb.r < 240 and color.rgb.g < 240 and color.rgb.b < 240:
        colors.append(color.rgb)


def draw_row(tur, x, y, col):
    tur.goto(x, y)
    for _ in range(10):
        tur.dot(20, r.choice(col))
        tur.forward(50)


tim = t.Turtle()
t.colormode(255)
t.setup(550, 550)
tim.speed('fastest')
tim.up()
tim.hideturtle()

for n in range(10):
    draw_row(tim, -225, -225 + n * 50, colors)

screen = t.Screen()
screen.exitonclick()
