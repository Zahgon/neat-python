
import gzip
import pickle
import random
import time

from neat.population import Population
from neat.reporting import BaseReporter


class Checkpointer(BaseReporter):

    def __init__(self, generation_interval, time_interval_seconds=None,
                 filename_prefix='neat-checkpoint-'):
        """
        Saves the current state (at the end of a generation) every ``generation_interval`` generations or
        ``time_interval_seconds``, whichever happens first.

        The checkpoint filename suffix (for example, ``neat-checkpoint-10``) always refers to the
        **next generation to be evaluated**.  In other words, a checkpoint created with suffix ``N``
        contains the population and species state for generation ``N`` at the point just before
        its fitness evaluation begins.

        :param generation_interval: If not None, maximum number of generations between save intervals,
                                    measured in generations-to-be-evaluated
        :type generation_interval: int or None
        :param time_interval_seconds: If not None, maximum number of seconds between checkpoint attempts
        :type time_interval_seconds: float or None
        :param str filename_prefix: Prefix for the filename (the end will be the generation number)
        """
        self.generation_interval = generation_interval
        self.time_interval_seconds = time_interval_seconds
        self.filename_prefix = filename_prefix

        self.current_generation = None
        self.last_generation_checkpoint = 0
        self.last_time_checkpoint = time.time()

    def start_generation(self, generation):
        pass

    def end_generation(self, config, population, species_set):
        pass

    def save_checkpoint(self, config, population, species_set, generation):
        pass

    @staticmethod
    def restore_checkpoint(filename, new_config=None):
        pass
