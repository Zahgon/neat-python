
import math
import random
from itertools import count

from neat.config import ConfigParameter, DefaultClassConfig
from neat.innovation import InnovationTracker
from neat.math_util import mean




class DefaultReproduction(DefaultClassConfig):

    @classmethod
    def parse_config(cls, param_dict):
        pass

    def __init__(self, config, reporters, stagnation):
        self.reproduction_config = config
        self.reporters = reporters
        self.genome_indexer = count(1)
        self.stagnation = stagnation
        self.ancestors = {}
        
        self.innovation_tracker = InnovationTracker()

    def create_new(self, genome_type, genome_config, num_genomes):
        pass

    @staticmethod
    def compute_spawn(adjusted_fitness, previous_sizes, pop_size, min_species_size):
        pass

    def _adjust_spawn_exact(self, spawn_amounts, pop_size, min_species_size):
        pass

    def reproduce(self, config, species, pop_size, generation):
        pass
