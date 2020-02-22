import math
from itertools import accumulate
from random import random


class CannonBall:
    def __init__(self, v, theta):
        self.v = v
        self.theta = theta
        self.x_hit = 0
        self.y = 0
        self.calculate_fitness()
        self.escaped = (self.x_hit == 0 or self.x_hit == WIDTH) and (self.x_hit > HEIGHT)

    def calculate_fitness(self):
        """
        x = v * t * cos(theta)
        t = 5 / (v * cons(theta))
        y = v * t * sin(theta) - 1/2 * g * t^2
        :return:
        """
        x = 0.5 * WIDTH
        x_hit = WIDTH
        if self.theta > math.pi / 2:
            x = -x
            x_hit = 0
        t = x / (self.v * math.cos(self.theta))
        y = self.v * t * math.sin(self.theta) - 0.5 * 9.81 * t ** 2
        if y < 0:
            y = 0.0
        self.x_hit = x_hit
        self.y = y

    def __repr__(self):
        return f"x_hit: {self.x_hit}, y: {self.y}"


def random_tries(n):
    gen = [CannonBall(v = int(random()*100), theta=random()*math.pi) for _ in range(n)]
    return gen


def selection(gen):
    results = [cannon_ball.y for cannon_ball in gen]
    return accumulate(results)


def crossover(gen):
    return gen


def mutate(gen):
    return gen


def display(gen):
    print(list(selection(gen)))
    print(gen)


if __name__ == '__main__':
    WIDTH = 30
    HEIGHT = 30
    ITEMS = 12
    EPOCHS = 10
    generation = random_tries(ITEMS)
    for _ in range(EPOCHS):
        generation = crossover(generation)
        mutate(generation)
    display(generation)
