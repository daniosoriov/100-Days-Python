import turtle as t

tim = t.Turtle()
t.listen()


def move_forward():
    tim.forward(10)


def turn_left():
    tim.left(10)


def turn_right():
    tim.right(10)


def move_back():
    tim.back(10)


def clear_screen():
    tim.clear()
    tim.speed(0)
    tim.up()
    tim.home()
    tim.down()
    tim.speed(6)


screen = t.Screen()
screen.listen()
screen.onkeypress(fun=move_forward, key='w')
screen.onkeypress(fun=turn_left, key='a')
screen.onkeypress(fun=turn_right, key='d')
screen.onkeypress(fun=move_back, key='s')
screen.onkeypress(fun=clear_screen, key='c')
screen.exitonclick()