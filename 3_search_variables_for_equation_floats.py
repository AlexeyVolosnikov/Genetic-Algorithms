### This algorithm written as an example of how
### genetic algorithm could\shoud work
###
### Here it solves a little problem of finding variables of equation (see equation function)
### Data type of variables is float

### Do not change gene_number
### Change only chromosome number, mutation chance and limit


from random import uniform
from random import randint
import os


class GeneticAlgorithm:
    """
    Genetic algorithms are commonly used to generate
    high-quality solutions to optimization and search problems

    :param gene_number       is a number of genes
    :param chromosome_number is a number of chomosomes
    :param value_needed      is a value closer to which result should be
    :param limit             is optional value, sets limit of iterations (executed loop will be for loop), if limit is not set
                             it automatically sets limit as infinity (in this case loop will be while loop)

    Pseudocode:
    START
        Generate the initial population
        Compute fitness
        REPEAT
            Selection
            Crossover
            Mutation
            Compute fitness
        UNTIL population has converged
    STOP

    """

    def __init__(self, gene_number, chromosome_number, mutation_chance, limit):
        self.chromosomes_for_filter = chromosome_number
        l = self.initialize_population(gene_number, chromosome_number)
        # probabilities = self.fitness(l)
        print('Start : ')
        for i, chromosome in enumerate(l):
            print(f'#{i} {chromosome} val : {self.equation(chromosome[0], chromosome[1], chromosome[2])}')

        l, probabilities = self.fitness(l)
        for i_to_limit in range(limit):
            _l = self.crossover(l)
            _l = self.mutation(_l, mutation_chance)
            _l, probabilities = self.fitness(_l)
            l = _l
            # print(f'iter {i_to_limit} / {limit}')

        print('Result : ')
        for i, chromosome in enumerate(l):
            print(f'#{i} {chromosome} val : {self.equation(chromosome[0], chromosome[1], chromosome[2])}')

    def initialize_population(self, gene_number, chromosome_number):
        """
        Initializing population to work with
        :return: list with population (Chomosomes and genes)
        """
        l = []
        for chromosome in range(chromosome_number):
            l.append([])
            for gene in range(gene_number):
                l[-1].append(round(uniform(0.01, 100), 2))
        return l

    def equation(self, x, y, z):
        return (3*(x**4) + 2*(x**2) + y) / (z**2)

    def fitness(self, l):
        """
        It is vitally important function, which defines are parameters
        fit or not for the solution
        :param l: list with  population
        :return: probability that individual will be selected for further reproduction
        """

        values = {}
        for i, chromosome in enumerate(l):
            values[i] = self.equation(chromosome[0], chromosome[1], chromosome[2]) # index : value

        _values = []

        for index in values:
            _values.append((index, values[index]))

        probabilities = [] # now in probabilities the less 1 val is better
        for index, eqvalue in _values:
            probabilities.append((index, abs(eqvalue-11)))

        probabilities.sort(key=lambda tup: tup[1])
        probabilities = probabilities[:self.chromosomes_for_filter]

        _l = []
        for index, percentage in probabilities:
            _l.append(l[index])

        return _l, probabilities

    def crossover(self, l):
        """
        Get all off-springs  (population size = a(i) ... a(i+1) )
        Here we use 'One Point Crossover'

        :return: new l
        """
        _l = []
        for i, chromosome_i in enumerate(l):
            for j in range(i + 1, len(l)):
                parent_1 = l[i]
                parent_2 = l[j]
                new_parent_1_left = l[i][:len(l[i])//2]
                new_parent_1_right = l[j][len(l[i])//2:]
                new_parent_2_left = l[j][:len(l[j])//2]
                new_parent_2_right = l[i][len(l[j])//2:]
                new_parent_1 = []
                new_parent_1.extend(new_parent_1_left)
                new_parent_1.extend(new_parent_1_right)
                new_parent_2 = []
                new_parent_2.extend(new_parent_2_left)
                new_parent_2.extend(new_parent_2_right)
                _l.append(new_parent_1)
                _l.append(new_parent_2)

        return _l

    def mutation(self, _l, mutation_chance):
        """
        For some chromosomes add mutation
        :return: list with mutated chromosomes
        """

        # mutation_chance = mutation_chance*100
        for i, chromosome in enumerate(_l):
            if round(uniform(0, 1), 2) <= mutation_chance: # 2 because it is mutation
                # mutate
                _l[i][randint(0, len(chromosome)) - 1] = round(uniform(0.01, 100), 2)

        return _l

import time
start = time.perf_counter()
GeneticAlgorithm(gene_number=3, chromosome_number=10, mutation_chance=0.01, limit=30000)
print(f'finished in {round(time.perf_counter() - start)} sec')
