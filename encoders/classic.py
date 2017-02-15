import random as rand

import numpy as np
from compute.adders import combine

seed = 20170131
# rand.seed(seed)


class ClassicEncoder(object):
    """
    Creates a number of random mappings from a vector of size input_size
    on to a vector of size input_area
    with offset input_offset,
    and adds padding of 0's up to size automaton_area.

    If random_mappings=3, input_size=4,
    then translations of new size 4 configurations will be of size 3*4=12
    """

    def __init__(self, n_random_mappings, input_size, input_area, automaton_area, input_offset=0, verbose=0):
        """

        :param n_random_mappings: the number of random mappings (0 is none)
        :param input_size: the size that the configurations come in
        :param input_area: the area/size that the inputs are to be mapped to
        :param automaton_area: the size of the whole automaton
        :param input_offset: offset for the mapping
        """
        self.random_mappings = []
        self.input_size = input_size
        self.input_area = max([input_size, input_area])
        self.automaton_area = max([self.input_area, automaton_area])
        self.verbose = verbose

        if n_random_mappings > 0:
            for _ in xrange(n_random_mappings):
                self.random_mappings.extend(make_random_mapping(input_size, self.input_area, input_offset))
        else:
            self.random_mappings.append([i for i in xrange(input_size)])

        if self.verbose > 1:
            print "Random mappings:"
            print self.random_mappings

    def translate(self, configurations):
        n_configurations = configurations.shape[0]
        translated_configs = np.empty((n_configurations, self.n_random_mappings, self.automaton_area), dtype='int')
        for i, config in enumerate(configurations):
            partial_translated_config = np.zeros(self.n_random_mappings * self.automaton_area, dtype='int')
            translated_configs[i] = self.overwrite(config, partial_translated_config)

        return translated_configs.reshape((self.n_random_mappings * n_configurations, self.automaton_area))

    def overwrite(self, master, second):
        """A method of adding vectors.
        Master overwrites second according to the mapping/translation.

        :param master: the unmapped master or input vector
        :param second: the already mapped vector that is to be overwritten (must already be a duplicate)
        :return: added vectors
        """
        automaton_offset = 0  # Offset index
        for i, r in enumerate(self.random_mappings):
            master_i = i % self.input_size
            second[automaton_offset + r] = master[master_i]

            if master_i + 1 == self.input_size:
                automaton_offset += self.automaton_area  # Adjusting offset

        return second.reshape(self.n_random_mappings, self.automaton_area)

    def normalized_addition(self, master, second):
        """A method of adding vectors.
        Yilmaz' (2015) normalized addition.

        :param master:
        :param second:
        :return:
        """
        empty = np.zeros(self.n_random_mappings * self.automaton_area, dtype='int')
        mapped_master = self.overwrite(master, empty)
        shape = mapped_master.shape
        return combine(mapped_master.ravel(), second).reshape(shape[0], shape[1])

    def pos(self, element):
        """Get what positions an element has

        :return: the position of all the element's mapping
        """
        return [pos[element] for pos in self.random_mappings]

    def mappings(self):
        return self.random_mappings

    @property
    def n_random_mappings(self):
        """The number of random mappings"""
        return len(self.random_mappings) / self.input_size

    @property
    def total_area(self):
        """The area of all automata"""
        return self.automaton_area * self.n_random_mappings


def make_random_mapping(input_size, input_area, input_offset=0):
    """Generates a pseudo-random mapping from inputs to outputs.
    The encoding stage.

    :param input_size: the size that the inputs come in
    :param input_area: the area/size that the inputs are to be mapped to
    :param input_offset: a number if an offset is wanted, default 0
    :return: an array of mapped indexes
    """
    input_indexes = []
    for i in xrange(input_size):
        # Going through all states in the reservoir
        # Might be possible to improve
        index = rand.randint(0, input_area - 1)
        while index in input_indexes:
            index = rand.randint(0, input_area - 1)
        input_indexes.append(index)
    return [i + input_offset for i in input_indexes]

