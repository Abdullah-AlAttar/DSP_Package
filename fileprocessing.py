
import numpy as np


def read_file(path):
    return np.array([int(line) for line in open(path)])


# x = read_file('./data/file1.txt')
