
from __future__ import annotations

import os
import warnings
from configparser import ConfigParser
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Mapping, Optional, Type


@dataclass(eq=False)
class ConfigParameter:

    name: str
    value_type: Type[Any]
    default: Any = None
    optional: bool = False  # If True, parameter can be omitted from config

    def __repr__(self) -> str:
        if self.default is None:
            return f"ConfigParameter({self.name!r}, {self.value_type!r})"
        return f"ConfigParameter({self.name!r}, {self.value_type!r}, {self.default!r})"

    def parse(self, section: str, config_parser: ConfigParser) -> Any:
        pass

    def interpret(self, config_dict: Mapping[str, Any], section_name: Optional[str] = None) -> Any:
        pass

    def format(self, value: Any) -> str:
        pass


def write_pretty_params(f, config: Any, params: Iterable[ConfigParameter]) -> None:
    param_names = [p.name for p in params]
    longest_name = max(len(name) for name in param_names)
    param_names.sort()
    param_lookup: Dict[str, ConfigParameter] = {p.name: p for p in params}

    for name in param_names:
        p = param_lookup[name]
        f.write(f'{p.name.ljust(longest_name)} = {p.format(getattr(config, p.name))}\n')


class UnknownConfigItemError(NameError):
    pass


class DefaultClassConfig:

    def __init__(self, param_dict, param_list, section_name=None):
        self._params = param_list
        self._section_name = section_name
        param_list_names = []
        for p in param_list:
            setattr(self, p.name, p.interpret(param_dict, section_name))
            param_list_names.append(p.name)
        unknown_list = [x for x in param_dict if x not in param_list_names]
        if unknown_list:
            if len(unknown_list) > 1:
                raise UnknownConfigItemError("Unknown configuration items:\n" +
                                             "\n\t".join(unknown_list))
            raise UnknownConfigItemError(f"Unknown configuration item {unknown_list[0]!s}")

    @classmethod
    def write_config(cls, f, config):
        pass


class Config:

    __params = [ConfigParameter('pop_size', int),
                ConfigParameter('fitness_criterion', str),
                ConfigParameter('fitness_threshold', float),
                ConfigParameter('reset_on_extinction', bool),
                ConfigParameter('no_fitness_termination', bool, False),
                ConfigParameter('seed', int, None, optional=True)]

    def __init__(self, genome_type, reproduction_type, species_set_type, stagnation_type, filename, config_information=None):
        assert hasattr(genome_type, 'parse_config')
        assert hasattr(reproduction_type, 'parse_config')
        assert hasattr(species_set_type, 'parse_config')
        assert hasattr(stagnation_type, 'parse_config')

        self.genome_type = genome_type
        self.reproduction_type = reproduction_type
        self.species_set_type = species_set_type
        self.stagnation_type = stagnation_type
        self.config_information = config_information

        if not os.path.isfile(filename):
            raise Exception('No such config file: ' + os.path.abspath(filename))

        parameters = ConfigParser()
        with open(filename) as f:
            parameters.read_file(f)

        if not parameters.has_section('NEAT'):
            raise RuntimeError("'NEAT' section not found in NEAT configuration file.")

        param_list_names = []
        for p in self.__params:
            try:
                setattr(self, p.name, p.parse('NEAT', parameters))
            except Exception as e:
                if p.optional:
                    setattr(self, p.name, p.default)
                elif p.default is None:
                    raise
                else:
                    raise RuntimeError(
                        f"Missing required configuration item in [NEAT] section: '{p.name}'\n"
                        f"This parameter must be explicitly specified in your configuration file.\n"
                        f"Suggested value: {p.name} = {p.default}"
                    ) from e
            param_list_names.append(p.name)
        param_dict = dict(parameters.items('NEAT'))
        unknown_list = [x for x in param_dict if x not in param_list_names]
        if unknown_list:
            if len(unknown_list) > 1:
                raise UnknownConfigItemError("Unknown (section 'NEAT') configuration items:\n" + "\n\t".join(unknown_list))
            raise UnknownConfigItemError(f"Unknown (section 'NEAT') configuration item {unknown_list[0]!s}")

        genome_dict = dict(parameters.items(genome_type.__name__))
        self.genome_config = genome_type.parse_config(genome_dict)

        species_set_dict = dict(parameters.items(species_set_type.__name__))
        self.species_set_config = species_set_type.parse_config(species_set_dict)

        stagnation_dict = dict(parameters.items(stagnation_type.__name__))
        self.stagnation_config = stagnation_type.parse_config(stagnation_dict)

        reproduction_dict = dict(parameters.items(reproduction_type.__name__))
        self.reproduction_config = reproduction_type.parse_config(reproduction_dict)

    def save(self, filename):
        pass
