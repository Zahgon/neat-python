from itertools import count

from neat.config import ConfigParameter, DefaultClassConfig
from neat.math_util import mean, stdev


class Species:
    def __init__(self, key, generation):
        self.key = key
        self.created = generation
        self.last_improved = generation
        self.representative = None
        self.members = {}
        self.fitness = None
        self.adjusted_fitness = None
        self.fitness_history = []

    def update(self, representative, members):
        self.representative = representative
        self.members = members

    def get_fitnesses(self):
        return [m.fitness for m in self.members.values()]


class GenomeDistanceCache:
    def __init__(self, config):
        self.distances = {}
        self.config = config
        self.hits = 0
        self.misses = 0

    def __call__(self, genome0, genome1):
        g0 = genome0.key
        g1 = genome1.key
        d = self.distances.get((g0, g1))
        if d is None:
            d = genome0.distance(genome1, self.config)
            self.distances[g0, g1] = d
            self.distances[g1, g0] = d
            self.misses += 1
        else:
            self.hits += 1

        return d


class DefaultSpeciesSet(DefaultClassConfig):

    def __init__(self, config, reporters):
        self.species_set_config = config
        self.reporters = reporters
        self.indexer = count(1)
        self.species = {}
        self.genome_to_species = {}

    @classmethod
    def parse_config(cls, param_dict):
        pass

    def speciate(self, config, population, generation):
        pass

    def get_species_id(self, individual_id):
        pass

    def get_species(self, individual_id):
        pass

    def __getstate__(self):
        """Prepare species set for pickling by converting indexer to a picklable form."""
        state = self.__dict__.copy()
        if self.indexer is not None:
            state['_indexer_next_value'] = next(self.indexer)
            state['indexer'] = None
        else:
            state['_indexer_next_value'] = None
        return state

    def __setstate__(self, state):
        """Restore species set from pickled state, recreating indexer."""
        _indexer_next_value = state.pop('_indexer_next_value', None)
        self.__dict__.update(state)
        if _indexer_next_value is not None:
            self.indexer = count(_indexer_next_value)
        else:
            self.indexer = None
