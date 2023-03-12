import turtle as t
import random as r


def draw_square(tur):
    # Drawing a square
    for _ in range(4):
        tur.forward(100)
        tur.left(90)


def draw_dash_line(tur, steps=15):
    # Drawing a dashed line
    for _ in range(steps):
        tur.forward(10)
        tur.up()
        tur.forward(10)
        tur.down()


def random_color():
    color = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
    return color


def draw_polygon(tur, sides=3, color="#000000"):
    angle = 360 / sides
    tur.color(color)
    for _ in range(sides):
        tur.forward(100)
        tur.left(angle)


def random_walk(tur, color="#000000"):
    tur.forward(50)
    tur.pencolor(color)
    tur.setheading(r.choice((0, 90, 180, 270)))


def draw_spirograph(tur, ratio, step):
    for _ in range(360 // step):
        tur.color(random_color())
        tur.circle(ratio)
        tur.left(step)


tim = t.Turtle()
t.colormode(255)
tim.shape('turtle')
tim.speed('fastest')

# Drawing a random walk
# tim.pensize(15)
# for _ in range(200):
#     random_walk(tim, random_color())

# Drawing polygons
# for n in range(3, 10):
#     draw_polygon(tim, n, random_color())

# Drawing a spirograph

draw_spirograph(tim, 25, 9)
draw_spirograph(tim, 50, 8)
draw_spirograph(tim, 75, 7)
draw_spirograph(tim, 100, 8)

# circles = 80
# angle = 360 / circles
# for _ in range(80):
#     tim.color(random_color())
#     tim.circle(100)
#     tim.left(angle)


screen = t.Screen()
screen.exitonclick()
