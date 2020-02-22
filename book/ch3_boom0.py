def random_tries(n):
    gen = [""] * n
    return gen


def crossover(gen):
    return gen


def mutate(gen):
    return gen


def display(gen):
    print(gen)


if __name__ == '__main__':

    ITEMS = 12
    EPOCHS = 10
    generation = random_tries(ITEMS)
    for _ in range(EPOCHS):
        generation = crossover(generation)
        mutate(generation)
    display(generation)
