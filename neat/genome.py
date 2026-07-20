import copy
import sys
from itertools import count
from random import choice, random, shuffle

from neat.activations import ActivationFunctionSet
from neat.aggregations import AggregationFunctionSet
from neat.config import ConfigParameter, write_pretty_params
from neat.genes import DefaultConnectionGene, DefaultNodeGene
from neat.graphs import creates_cycle
from neat.graphs import required_for_output


class DefaultGenomeConfig:
    allowed_connectivity = ['unconnected', 'fs_neat_nohidden', 'fs_neat', 'fs_neat_hidden',
                            'full_nodirect', 'full', 'full_direct',
                            'partial_nodirect', 'partial', 'partial_direct']

    def __init__(self, params, section_name='DefaultGenome'):
        self.activation_defs = ActivationFunctionSet()
        self.aggregation_function_defs = AggregationFunctionSet()
        self.aggregation_defs = self.aggregation_function_defs

        self._params = [ConfigParameter('num_inputs', int),
                        ConfigParameter('num_outputs', int),
                        ConfigParameter('num_hidden', int),
                        ConfigParameter('feed_forward', bool),
                        ConfigParameter('compatibility_disjoint_coefficient', float),
                        ConfigParameter('compatibility_weight_coefficient', float),
                        ConfigParameter('conn_add_prob', float),
                        ConfigParameter('conn_delete_prob', float),
                        ConfigParameter('node_add_prob', float),
                        ConfigParameter('node_delete_prob', float),
                        ConfigParameter('single_structural_mutation', bool, 'false'),
                        ConfigParameter('structural_mutation_surer', str, 'default'),
                        ConfigParameter('initial_connection', str, 'unconnected')]

        self.node_gene_type = params['node_gene_type']
        self._params += self.node_gene_type.get_config_params()
        self.connection_gene_type = params['connection_gene_type']
        self._params += self.connection_gene_type.get_config_params()

        for p in self._params:
            setattr(self, p.name, p.interpret(params, section_name))

        self.node_gene_type.validate_attributes(self)
        self.connection_gene_type.validate_attributes(self)

        self.input_keys = [-i - 1 for i in range(self.num_inputs)]
        self.output_keys = [i for i in range(self.num_outputs)]

        self.connection_fraction = None

        if 'partial' in self.initial_connection:
            c, p = self.initial_connection.split()
            self.initial_connection = c
            self.connection_fraction = float(p)
            if not (0 <= self.connection_fraction <= 1):
                raise RuntimeError(
                    "'partial' connection value must be between 0.0 and 1.0, inclusive.")

        assert self.initial_connection in self.allowed_connectivity

        if self.structural_mutation_surer.lower() in ['1', 'yes', 'true', 'on']:
            self.structural_mutation_surer = 'true'
        elif self.structural_mutation_surer.lower() in ['0', 'no', 'false', 'off']:
            self.structural_mutation_surer = 'false'
        elif self.structural_mutation_surer.lower() == 'default':
            self.structural_mutation_surer = 'default'
        else:
            error_string = f"Invalid structural_mutation_surer {self.structural_mutation_surer!r}"
            raise RuntimeError(error_string)

        self.node_indexer = None
        
        self.innovation_tracker = None

    def add_activation(self, name, func):
        pass

    def add_aggregation(self, name, func):
        pass

    def save(self, f):
        pass

    def get_new_node_key(self, node_dict):
        pass

    def check_structural_mutation_surer(self):
        pass

    def __getstate__(self):
        """Prepare config for pickling by converting node_indexer to a picklable form."""
        state = self.__dict__.copy()
        if self.node_indexer is not None:
            state['_node_indexer_next_value'] = next(self.node_indexer)
            state['node_indexer'] = None
        else:
            state['_node_indexer_next_value'] = None
        return state

    def __setstate__(self, state):
        """Restore config from pickled state, recreating node_indexer."""
        _node_indexer_next_value = state.pop('_node_indexer_next_value', None)
        self.__dict__.update(state)
        if _node_indexer_next_value is not None:
            self.node_indexer = count(_node_indexer_next_value)
        else:
            self.node_indexer = None


class DefaultGenome:

    @classmethod
    def parse_config(cls, param_dict):
        pass

    @classmethod
    def write_config(cls, f, config):
        pass

    def __init__(self, key):
        self.key = key

        self.connections = {}
        self.nodes = {}

        self.fitness = None

    def configure_new(self, config):
        pass

    def configure_crossover(self, genome1, genome2, config):
        pass

    def mutate(self, config):
        pass

    def mutate_add_node(self, config):
        pass

    def add_connection(self, config, input_key, output_key, weight, enabled, innovation=None):
        pass

    def mutate_add_connection(self, config):
        pass

    def mutate_delete_node(self, config):
        pass

    def mutate_delete_connection(self):
        pass

    def distance(self, other, config):
        pass

    def size(self):
        pass

    def __str__(self):
        s = f"Key: {self.key}\nFitness: {self.fitness}\nNodes:"
        for k, ng in self.nodes.items():
            s += f"\n\t{k} {ng!s}"
        s += "\nConnections:"
        connections = list(self.connections.values())
        connections.sort()
        for c in connections:
            s += "\n\t" + str(c)
        return s

    @staticmethod
    def create_node(config, node_id):
        pass

    @staticmethod
    def create_connection(config, input_id, output_id, innovation):
        pass

    def connect_fs_neat_nohidden(self, config):
        pass

    def connect_fs_neat_hidden(self, config):
        pass

    def compute_full_connections(self, config, direct):
        pass

    def connect_full_nodirect(self, config):
        pass

    def connect_full_direct(self, config):
        pass

    def connect_partial_nodirect(self, config):
        pass

    def connect_partial_direct(self, config):
        pass

    def get_pruned_copy(self, genome_config):
        pass


def get_pruned_genes(node_genes, connection_genes, input_keys, output_keys):
    pass
