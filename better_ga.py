import numpy as np
import matplotlib.pyplot as plt

from data.eu_measurments import get_eu_measurments

data = get_eu_measurments()


# Fitness function stays the same
def fitness_function(data, pop):
    fitness = []
    for solution in range(len(pop)):
        for event in range(len(data)):
            error = 0
            event_time = data[event][0]
            event_measured = data[event][1]
            event_expected = pop[solution][0] * event_time ** 3 + \
                             pop[solution][1] * event_time ** 2 + \
                             pop[solution][2] * event_time + pop[solution][3]
            error += (event_expected - event_measured) ** 2
        fitness.append(1 / error)
        # We use 1/error in order to use a maximization mechanism, while we want to minimize the error
    return fitness


def biased_selection(pop, fitness, num_parents):
    # Select parents randomly, with chance proportional to their fitness
    selected_indices = np.random.choice(pop.shape[0], num_parents, p=(fitness / np.sum(fitness)))
    return pop[selected_indices, :]


def recombination(parents, offspring_size):
    offspring = np.empty(offspring_size)
    for k in range(offspring_size[0]):
        # Pick a random recombination point for each offspring
        # (rather than recombining right in the middle of the chromosome)
        recombination_point = np.random.randint(0, offspring_size[1])
        parent1_idx = k % parents.shape[0]
        parent2_idx = (k + 1) % parents.shape[0]
        offspring[k, 0:recombination_point] = parents[parent1_idx, 0:recombination_point]
        offspring[k, recombination_point:] = parents[parent2_idx, recombination_point:]
    return offspring


def mutation(offspring_recombination, generation, number_of_generations):
    max_mutation_scale = 150
    # Make mutation scale decrease linearly as the generations progress
    mutation_scale = max_mutation_scale * ((number_of_generations - generation) / number_of_generations)
    for idx in range(offspring_recombination.shape[0]):
        random_value = np.random.randint(-mutation_scale, mutation_scale, 1)
        random_index = np.random.randint(0, offspring_recombination.shape[1], 1)
        offspring_recombination[idx, random_index] = offspring_recombination[idx, random_index] + random_value
    return offspring_recombination


# GA Parameters
formula_degree = 4
number_of_solutions = 800
number_of_parents = 350
population_size = (number_of_solutions, formula_degree)
number_of_generations = 20
best_outputs = []

# Genesis
new_population = np.random.randint(low=0, high=10000, size=population_size)
print("The population of the first generation: ")
print(new_population)

# Evolution
print("\nEvolution:")
for generation in range(number_of_generations):
    fitness = fitness_function(data, new_population)
    print("Generation = ", generation, "\tBest fitness = ", round(1 / np.max(fitness), 5))
    # best_outputs.append(np.max(np.sum(new_population*formula_degree, axis=1)))
    best_outputs.append(round(1 / np.max(fitness), 5))
    parents = biased_selection(new_population, fitness, number_of_parents)
    offspring_recombination = recombination(parents,
                                            offspring_size=(population_size[0] - parents.shape[0], formula_degree))
    offspring_mutation = mutation(offspring_recombination, generation, number_of_generations)
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation
    # Stop the process if at least 10 generations passed
    # and there's no improvement in the past 5 generations
    if generation >= 10:
        if best_outputs[generation] == best_outputs[generation - 5]:
            break

# Results
print("\nThe population of the last generation: ")
print(new_population)
fitness = fitness_function(data, new_population)
best_match_idx = np.where(fitness == np.max(fitness))
print("Best solution: \n", np.unique(new_population[best_match_idx, :][0]))

# Chart
plt.plot(best_outputs)
plt.xlabel("Generation")
plt.ylabel("Best Fitness Score")
plt.show()
