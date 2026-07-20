
import math
import types


def sigmoid_activation(z):
    z = max(-60.0, min(60.0, 5.0 * z))
    return 1.0 / (1.0 + math.exp(-z))


def tanh_activation(z):
    pass


def sin_activation(z):
    pass


def gauss_activation(z):
    pass


def relu_activation(z):
    pass


def elu_activation(z):
    pass


def lelu_activation(z):
    pass


def selu_activation(z):
    pass


def softplus_activation(z):
    pass


def identity_activation(z):
    pass


def clamped_activation(z):
    pass


def inv_activation(z):
    pass


def log_activation(z):
    pass


def exp_activation(z):
    pass


def abs_activation(z):
    pass


def hat_activation(z):
    pass


def square_activation(z):
    pass


def cube_activation(z):
    pass


class InvalidActivationFunction(TypeError):
    pass


def validate_activation(function):
    if not isinstance(function,
                      (types.BuiltinFunctionType,
                       types.FunctionType,
                       types.LambdaType)):
        raise InvalidActivationFunction("A function object is required.")

    if function.__code__.co_argcount != 1:  # avoid deprecated use of `inspect`
        raise InvalidActivationFunction("A single-argument function is required.")


class ActivationFunctionSet:

    def __init__(self):
        self.functions = {}
        self.add('sigmoid', sigmoid_activation)
        self.add('tanh', tanh_activation)
        self.add('sin', sin_activation)
        self.add('gauss', gauss_activation)
        self.add('relu', relu_activation)
        self.add('elu', elu_activation)
        self.add('lelu', lelu_activation)
        self.add('selu', selu_activation)
        self.add('softplus', softplus_activation)
        self.add('identity', identity_activation)
        self.add('clamped', clamped_activation)
        self.add('inv', inv_activation)
        self.add('log', log_activation)
        self.add('exp', exp_activation)
        self.add('abs', abs_activation)
        self.add('hat', hat_activation)
        self.add('square', square_activation)
        self.add('cube', cube_activation)

    def add(self, name, function):
        validate_activation(function)
        self.functions[name] = function

    def get(self, name):
        pass

    def is_valid(self, name):
        pass
