import turtle
import random

SIDE_SIZE = 70
RIGHT_ANGLE = 90


def draw_bag():
    turtle.shape('turtle')
    turtle.pen(pencolor='brown', pensize=5)
    turtle.penup()
    turtle.goto(-SIDE_SIZE/2, SIDE_SIZE/2)
    turtle.pendown()
    turtle.right(RIGHT_ANGLE)
    turtle.forward(SIDE_SIZE)
    turtle.left(RIGHT_ANGLE)
    turtle.forward(SIDE_SIZE)
    turtle.left(RIGHT_ANGLE)
    turtle.forward(SIDE_SIZE)


def escaped(position):
    return any(any([i < -SIDE_SIZE/2, i > SIDE_SIZE/2]) for i in position)


def draw_line():
    angle = 0
    step = 20
    t = turtle.Turtle()
    while not escaped(t.position()):
        t.left(angle)
        t.forward(step)


def draw_square(t, size):
    L = []
    for i in range(4):
        t.forward(size)
        t.left(RIGHT_ANGLE)
        store_position_data(L, t)
    return L


def store_position_data(L, t):
    position = t.position()
    L.append([*position, escaped(position)])


def draw_squares(number, t):
    L = []
    for i in range(0, number, 10):
        t.penup()
        t.goto(-i, -i)
        if escaped(t.position()):
            return L
        t.pendown()
        L.extend(draw_square(t, i * 2))


def draw_squares_until_escaped(n):
    t = turtle.Turtle()

    L = draw_squares(n, t)
    with open("../data_square", "wt") as f:
        print(L, file=f)


def draw_triangles(number):
    t = turtle.Turtle()
    for i in range(number):
        t.forward(i*10)
        t.right(120)


def draw_spirals_until_escaped():
    t = turtle.Turtle()
    t.penup()
    t.left(random.randint(0, 360))
    t.pendown()

    i = 0
    turn = 360/random.randint(1, 10)
    L = []
    store_position_data(L, t)
    while not escaped(t.position()):
        i += 1
        t.forward(i*5)
        t.right(turn)
        store_position_data(L, t)

    return L


def draw_random_spirangles():
    L = []
    for i in range(100):
        L.extend(draw_spirals_until_escaped())
    with open("data_rand", "wt") as f:
        print(L, file=f)


if __name__ == '__main__':
    turtle.setworldcoordinates(-SIDE_SIZE, -SIDE_SIZE, SIDE_SIZE, SIDE_SIZE)
    draw_bag()
    # draw_squares_until_escaped(100)
    for _ in range(100):
        draw_spirals_until_escaped()

    turtle.mainloop()
