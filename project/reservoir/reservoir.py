import numpy as np
import random as rn
import scipy as sp
import ca.util as cutil


class Reservoir:
    # TODO maybe make it capable of delay (?) like Bye did

    def __init__(self, reservoir, iterations,  random_mappings, input_size, input_area, automaton_area, verbose=False):
        """

        :param reservoir: the CA object
        :param iterations: the number of iterations
        :param random_mappings: the number of random mappings (0 is none)
        :param input_size: the size that the configurations come in
        :param input_area: the area/size that the inputs are to be mapped to
        :param automaton_area: the size of the whole automaton
        """
        self.reservoir = reservoir
        self.iterations = iterations
        self.random_mappings = []
        self.input_area = max([input_size, input_area])
        self.automaton_area = max([self.input_area, automaton_area])
        self.verbose = verbose
        if random_mappings > 0:
            for _ in xrange(random_mappings):
                self.random_mappings.append(make_random_mapping(input_size, self.input_area))
        else:
            self.random_mappings.append([i for i in xrange(input_size)])

        print "Input size %d, %d iterations, %d random mappings, input area %d, automaton area %d" \
              % (input_size, self.iterations, random_mappings, self.input_area, self.automaton_area)

    def transform(self, configs):
        """Lets the reservoir digest each of the configurations.
        No training here.

        :param configs: a list of initial configurations
        :param external_input: a dictionary where one can alter states of the reservoir at specific time steps
        :return: a list in which each element is the output of a configuration
        """
        outputs = []
        for ci in xrange(len(configs)):
            # For every initial configuration

            config = configs[ci]
            concat = []

            if self.verbose:
                print ""
                print "NEW CONFIG:"
                cutil.print_config_1dim(config)
                print ""

            # Form a N * R vector in the beginning of CA evolution for this configuration
            mapped_config = sp.zeros([self.automaton_area * len(self.random_mappings)], dtype=np.dtype(int))
            for i, r in enumerate(self.random_mappings):
                for ri in xrange(len(r)):
                    mapped_config[self.automaton_area * i + r[ri]] = config[ri]

            if self.verbose:
                print "Mappings:", self.random_mappings
                cutil.print_config_1dim(mapped_config)
            # concat.extend(mapped_config)

            # Iterate
            for step in xrange(self.iterations):

                new_config = self.reservoir.step(mapped_config)
                if self.verbose:
                    cutil.print_config_1dim(new_config)
                # if step >= (self.iterations - 5):
                # Concatenating this new configuration to the vector
                concat.extend(new_config)
                mapped_config = new_config
            outputs.append(concat)

        if self.verbose:
            print "OUTPUT VECTORS"
            for o in outputs:
                cutil.print_config_1dim(o)
        return outputs

    def set_seed(self, seed):
        rn.seed(seed)


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
        index = rn.randint(0, input_area - 1)
        while index in input_indexes:
            index = rn.randint(0, input_area - 1)
        input_indexes.append(index)
    return [i + input_offset for i in input_indexes]

