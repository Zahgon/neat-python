
import types
import warnings
from functools import reduce
from operator import mul

from neat.math_util import mean, median2


def product_aggregation(x):  # note: `x` is a list or other iterable
    pass


def sum_aggregation(x):
    pass


def max_aggregation(x):
    pass


def min_aggregation(x):
    pass


def maxabs_aggregation(x):
    pass


def median_aggregation(x):
    pass


def mean_aggregation(x):
    pass


class InvalidAggregationFunction(TypeError):
    pass


def validate_aggregation(function):  # TODO: Recognize when need `reduce`
    if not isinstance(function,
                      (types.BuiltinFunctionType,
                       types.FunctionType,
                       types.LambdaType)):
        raise InvalidAggregationFunction("A function object is required.")

    if not (function.__code__.co_argcount >= 1):
        raise InvalidAggregationFunction("A function taking at least one argument is required")


class AggregationFunctionSet:

    def __init__(self):
        self.functions = {}
        self.add('product', product_aggregation)
        self.add('sum', sum_aggregation)
        self.add('max', max_aggregation)
        self.add('min', min_aggregation)
        self.add('maxabs', maxabs_aggregation)
        self.add('median', median_aggregation)
        self.add('mean', mean_aggregation)

    def add(self, name, function):
        validate_aggregation(function)
        self.functions[name] = function

    def get(self, name):
        pass

    def __getitem__(self, index):
        warnings.warn(f"Use get, not indexing ([{index!r}]), for aggregation functions",
                      DeprecationWarning)
        return self.get(index)

    def is_valid(self, name):
        pass
