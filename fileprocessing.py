
import numpy as np


def read_file(path):
    f = open(path)
    output = []
    for line in f:
        output.append(int(line))
    return output


# x = read_file('./data/file1.txt')
