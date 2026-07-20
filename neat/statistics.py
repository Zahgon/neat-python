import copy
import csv

from neat.math_util import mean, stdev, median2
from neat.reporting import BaseReporter



class StatisticsReporter(BaseReporter):

    def __init__(self):
        BaseReporter.__init__(self)
        self.most_fit_genomes = []
        self.generation_statistics = []

    def post_evaluate(self, config, population, species, best_genome):
        pass

    def get_fitness_stat(self, f):
        pass

    def get_fitness_mean(self):
        pass

    def get_fitness_stdev(self):
        pass

    def get_fitness_median(self):
        pass

    def best_unique_genomes(self, n):
        pass

    def best_genomes(self, n):
        pass

    def best_genome(self):
        pass

    def save(self):
        pass

    def save_genome_fitness(self,
                            delimiter=' ',
                            filename='fitness_history.csv'):
        pass

    def save_species_count(self, delimiter=' ', filename='speciation.csv'):
        pass

    def save_species_fitness(self, delimiter=' ', null_value='NA', filename='species_fitness.csv'):
        pass

    def get_species_sizes(self):
        pass

    def get_species_fitness(self, null_value=''):
        pass
