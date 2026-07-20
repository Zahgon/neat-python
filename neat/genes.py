import warnings
from random import random

from neat.attributes import FloatAttribute, BoolAttribute, StringAttribute




class BaseGene:

    def __init__(self, key):
        self.key = key

    def __str__(self):
        attrib = ['key']
        if hasattr(self, 'innovation'):
            attrib.append('innovation')
        attrib += [a.name for a in self._gene_attributes]
        attrib = [f'{a}={getattr(self, a)}' for a in attrib]
        return f'{self.__class__.__name__}({", ".join(attrib)})'

    def __lt__(self, other):
        assert isinstance(self.key, type(other.key)), f"Cannot compare keys {self.key!r} and {other.key!r}"
        return self.key < other.key

    @classmethod
    def parse_config(cls, config, param_dict):
        pass

    @classmethod
    def get_config_params(cls):
        pass

    @classmethod
    def validate_attributes(cls, config):
        pass

    def init_attributes(self, config):
        pass

    def mutate(self, config):
        pass

    def copy(self):
        if hasattr(self, 'innovation'):
            new_gene = self.__class__(self.key, innovation=self.innovation)
        else:
            new_gene = self.__class__(self.key)
        
        for a in self._gene_attributes:
            setattr(new_gene, a.name, getattr(self, a.name))

        return new_gene

    def crossover(self, gene2):
        pass




class DefaultNodeGene(BaseGene):
    _gene_attributes = [FloatAttribute('bias'),
                        FloatAttribute('response'),
                        StringAttribute('activation', options=''),
                        StringAttribute('aggregation', options=''),
                        FloatAttribute('time_constant',
                                       init_mean=1.0, init_stdev=0.0,
                                       replace_rate=0.0, mutate_rate=0.0,
                                       mutate_power=0.0,
                                       max_value=10.0, min_value=0.01)]

    def __init__(self, key):
        assert isinstance(key, int), f"DefaultNodeGene key must be an int, not {key!r}"
        BaseGene.__init__(self, key)

    def distance(self, other, config):
        pass


class DefaultConnectionGene(BaseGene):
    _gene_attributes = [FloatAttribute('weight'),
                        BoolAttribute('enabled')]

    def __init__(self, key, innovation=None):
        assert isinstance(key, tuple), f"DefaultConnectionGene key must be a tuple, not {key!r}"
        assert innovation is not None, "Innovation number is required for DefaultConnectionGene"
        assert isinstance(innovation, int), f"Innovation must be an int, not {type(innovation)}"
        BaseGene.__init__(self, key)
        self.innovation = innovation

    def distance(self, other, config):
        pass
    
    def __eq__(self, other):
        """Compare genes by innovation number."""
        if not isinstance(other, DefaultConnectionGene):
            return False
        return self.innovation == other.innovation
    
    def __hash__(self):
        """Hash by innovation number for use in sets/dicts."""
        return hash(self.innovation)
