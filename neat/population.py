
import random
from itertools import count

from neat.math_util import mean
from neat.reporting import ReporterSet


class CompleteExtinctionException(Exception):
    pass


class Population:

    def __init__(self, config, initial_state=None, seed=None):
        if seed is None and hasattr(config, 'seed'):
            seed = config.seed
        
        if seed is not None:
            random.seed(seed)
        
        self.reporters = ReporterSet()
        self.config = config
        stagnation = config.stagnation_type(config.stagnation_config, self.reporters)
        self.reproduction = config.reproduction_type(config.reproduction_config,
                                                     self.reporters,
                                                     stagnation)
        if config.fitness_criterion == 'max':
            self.fitness_criterion = max
        elif config.fitness_criterion == 'min':
            self.fitness_criterion = min
        elif config.fitness_criterion == 'mean':
            self.fitness_criterion = mean
        elif not config.no_fitness_termination:
            raise RuntimeError(
                f"Unexpected fitness_criterion: {config.fitness_criterion!r}")

        if initial_state is None:
            self.population = self.reproduction.create_new(config.genome_type,
                                                           config.genome_config,
                                                           config.pop_size)
            self.species = config.species_set_type(config.species_set_config, self.reporters)
            self.generation = 0
            self.species.speciate(config, self.population, self.generation)
        else:
            self.population, self.species, self.generation = initial_state
            self.species.reporters = self.reporters
            if hasattr(self.reproduction, "genome_indexer"):
                self.reproduction.genome_indexer = count(max(self.population.keys()) + 1)

        self.best_genome = None

    def add_reporter(self, reporter):
        pass

    def remove_reporter(self, reporter):
        pass

    def run(self, fitness_function, n=None):
        pass
