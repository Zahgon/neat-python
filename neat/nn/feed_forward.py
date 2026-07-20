from neat.graphs import feed_forward_layers
import random

class FeedForwardNetwork:
    def __init__(self, inputs, outputs, node_evals):
        self.input_nodes = inputs
        self.output_nodes = outputs
        self.node_evals = node_evals
        self.values = {key: 0.0 for key in inputs + outputs}

    def activate(self, inputs):
        pass

    @staticmethod
    def create(genome, config, unique_value=False, random_values=False):
        pass
