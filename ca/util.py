import random as rn
import math


def print_config_1dim(config):
    line = ""
    on = "  "
    off = unichr(0x2588) + unichr(0x2588)
    for i in xrange(config.size):
        line += on if config[i] == 0b1 else off
    print line


def init_config_simple(size=21, k=2):
    config = []
    for i in xrange(size):
        config.append(0b0)
    config[int(math.ceil(size/2))] = 0b1
    return config


def init_config_rand(size=20, k=2):
    # [0b0, 0b0, 0b0, 0b0, 0b0, 0b1, 0b0, 0b0, 0b0, 0b0, 0b0]
    config = []
    for i in xrange(size):
        config.append(rn.randint(0, k - 1))
    return config


def get_all_rules(k, n):
    """Many iterations.

    :param k: number of states
    :param n: number of neighbors
    """

    rules = []

    for x in xrange(k**(k**n)):
        rule = {}
        for y in xrange(k**n):
            rule[y] = 0b1 if x > 0 and x & 2**y == 2**y else 0b0
        rules.append(rule)

    return rules


def get_rule(rule=0, k=2, n=3):
    """Uses "brute force" to find the transition function for the rule number

    :param rule: the rule
    :param k: number of states
    :param n: number of neighbors
    """
    rules = get_all_rules(k, n)
    rule = rules[rule]

    return rule
