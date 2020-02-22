from turtle import (lt, rt, fd, mainloop)


def x(n):
    if n > 0:
        l("X+YF+", n)


def y(n):
    if n > 0:
        l("-FX-Y", n)


def l(s, n):
    for c in s:
        if c == "-":
            lt(90)
        elif c == "+":
            rt(90)
        elif c == "X":
            x(n - 1)
        elif c == "Y":
            y(n - 1)
        elif c == "F":
            fd(12)


if __name__ == '__main__':
    x(10)
    mainloop()
