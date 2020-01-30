import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt

from data.emr3d1 import get_emr3d1
from clustering_example import make_chart

data, variables1 = get_emr3d1()


def fitness_function(pop):
    """
    Here we define fitness as the ratio between
    the mean inter-cluster distance
    and mean intra-cluster distnace
    (the greater - the better)
    """
    fitness = []
    num_clusters = np.max(pop) + 1
    for solution in pop:
        centroids = np.zeros(shape=[num_clusters, 3])
        intra_cluster_dist_sum = 0
        for k in range(num_clusters):
            centroids[k] = np.mean(data[solution == k], axis=0)
            intra_cluster_dist_sum += np.sum(np.sqrt(np.sum(np.square(data[solution == k] - centroids[k]), axis=1)))
        mean_inter_cluster_dist = np.mean(distance.pdist(centroids))
        mean_intra_cluster_dist = intra_cluster_dist_sum / data.size
        fitness.append(mean_inter_cluster_dist / mean_intra_cluster_dist)
    return np.array(fitness)


def biased_selection(pop, fitness, num_parents, number_of_transporters=0):
    """Select parents randomly, with chance proportional to their fitness
    Return top n best genes as transporter
    """
    prob = fitness / np.sum(np.nan_to_num(fitness))
    prob[np.isnan(prob)] = 0
    top_n = np.argsort(fitness)[-number_of_transporters:]
    selected_indices = np.random.choice(pop.shape[0], num_parents, p=prob)
    return pop[selected_indices, :], pop[top_n, :]


def recombination(parents, offspring_size):
    offspring = np.empty(offspring_size)
    for k in range(offspring_size[0]):
        # Pick a random recombination point for each offspring
        # (rather than recombining right in the middle of the chromosome)
        recombination_point = np.random.randint(0, offspring_size[1])
        parent1_idx = k % parents.shape[0]
        parent2_idx = (k + 1) % parents.shape[0]
        offspring[k, :recombination_point] = parents[parent1_idx, :recombination_point]
        offspring[k, recombination_point:] = parents[parent2_idx, recombination_point:]
    return offspring


def mutation(offspring_recombination, p_mutation):
    """
    A mutation is a having a certain proportion of genes change their cluster assignment to a random value
    (could still be the same cluster - by chance)
    The proportion is defined by probability of mutation
    Mutated cluster having the porbbility based on current frequency in the population
    """
    original_shape = offspring_recombination.shape
    t = offspring_recombination.reshape(1, -1)
    positions = [np.random.randint(0, t.size, int(t.size * p_mutation))]
    clusters, counts = np.unique(offspring_recombination.reshape(1, -1), return_counts=True)
    cluster_prob = counts / counts.sum()
    cluster_mutations = np.random.choice(clusters, len(positions[0]), p=cluster_prob)
    t[:, positions] = cluster_mutations
    return t.reshape(original_shape)


# GA Parameters

# starting from some random number of clusters
starting_num_clusters = 5

number_of_transporters = 10
number_of_solutions = 2000
number_of_parents = 500
population_size = (number_of_solutions, data.shape[0])
number_of_generations = 500
P_mutation = 0.005
best_outputs = []


# Genesis
# We assign a cluster to each instance at random
new_population = np.random.randint(low=0, high=starting_num_clusters, size=population_size)
print("The population of the first generation: ")
print(new_population)

# Evolution
print("\nEvolution:")
for generation in range(number_of_generations):
    fitness = fitness_function(new_population)
    if generation % 10 == 0:
        print("Generation = ", generation, "\tBest fitness = ", round(np.max(np.nan_to_num(fitness)), 5))
    best_outputs.append(round(np.max(np.nan_to_num(fitness)), 5))
    # Stop the process if at least 50 generations passed
    # and there's no improvement in the past 25 generations
    if generation >= 50 and best_outputs[generation] == best_outputs[generation - 25]:
        break

    parents, top_n = biased_selection(new_population, fitness, number_of_parents, number_of_transporters)
    offspring_recombination = recombination(parents,
                                            offspring_size=(population_size[0] - parents.shape[0], data.shape[0]))
    offspring_mutation = mutation(offspring_recombination, P_mutation)
    new_population[:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation
    new_population = np.vstack([new_population[:number_of_solutions - number_of_transporters], top_n])

# Results
print("\nThe population of the last generation: ")
print(new_population)
fitness = fitness_function(new_population)
best_match_idx = np.where(fitness == np.max(np.nan_to_num(fitness)))
print("Best solution: \n", np.unique(new_population[best_match_idx, :][0], axis=0))

# Chart
plt.plot(best_outputs)
plt.xlabel("Generation")
plt.ylabel("Best Fitness Score")
plt.show()

make_chart(data, np.unique(new_population[best_match_idx, :][0], axis=0).ravel(), variables1)
