
import numpy as np

# f = open('./data/file1.txt')
# # print(f.readlines())
# x = [float(line) for line in f.readlines()]
# y = range(len(x))
# plt.plot(x,y)
# plt.show()
# print(l)


def read_file(path):
    return ([float(line) for line in open(path)])


# x = read_file('./data/file1.txt')
