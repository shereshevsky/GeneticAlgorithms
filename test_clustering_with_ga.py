import numpy as np
from unittest import TestCase
from clustering_with_ga import fitness_function



class Test(TestCase):
    def test_fitness_function(self):
        data = np.array([(0, 1), (0, 1), (1, 0)])
        pop = np.array([(0, 0, 1)])

        res = fitness_function(data, pop)
        assert res == np.array([0.])

        data = np.array([(1, 0), (1, 0), (1, 0)])
        pop = np.array([(0, 0, 1)])

        print(fitness_function(data, pop))