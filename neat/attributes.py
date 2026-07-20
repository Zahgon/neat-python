from copy import deepcopy
from random import choice, gauss, random, uniform, randint

from neat.config import ConfigParameter




class BaseAttribute:

    def __init__(self, name, **default_dict):
        self.name = name
        self._config_items = deepcopy(self.__class__._config_items)
        for n, default in default_dict.items():
            self._config_items[n] = [self._config_items[n][0], default]
        for n in self._config_items:
            setattr(self, n + "_name", self.config_item_name(n))

    def config_item_name(self, config_item_base_name):
        pass

    def get_config_params(self):
        pass


class FloatAttribute(BaseAttribute):
    _config_items = {"init_mean": [float, None],
                     "init_stdev": [float, None],
                     "init_type": [str, 'gaussian'],
                     "replace_rate": [float, None],
                     "mutate_rate": [float, None],
                     "mutate_power": [float, None],
                     "max_value": [float, None],
                     "min_value": [float, None]}

    def clamp(self, value, config):
        pass

    def init_value(self, config):
        pass

    def mutate_value(self, value, config):
        pass

    def validate(self, config):
        pass


class IntegerAttribute(BaseAttribute):
    _config_items = {"replace_rate": [float, None],
                     "mutate_rate": [float, None],
                     "mutate_power": [float, None],
                     "max_value": [int, None],
                     "min_value": [int, None]}

    def clamp(self, value, config):
        pass

    def init_value(self, config):
        pass

    def mutate_value(self, value, config):
        pass

    def validate(self, config):
        pass


class BoolAttribute(BaseAttribute):
    _config_items = {"default": [str, None],
                     "mutate_rate": [float, None],
                     "rate_to_true_add": [float, 0.0],
                     "rate_to_false_add": [float, 0.0]}

    def init_value(self, config):
        pass

    def mutate_value(self, value, config):
        pass

    def validate(self, config):
        pass


class StringAttribute(BaseAttribute):
    _config_items = {"default": [str, 'random'],
                     "options": [list, None],
                     "mutate_rate": [float, None]}

    def init_value(self, config):
        pass

    def mutate_value(self, value, config):
        pass

    def validate(self, config):
        pass
