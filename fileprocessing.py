
import numpy as np

# f = open('./data/file1.txt')
# # print(f.readlines())
# x = [float(line) for line in f.readlines()]
# y = range(len(x))
# plt.plot(x,y)
# plt.show()
# print(l)

from scipy.io import wavfile
import winsound
from playsound import playsound


def read_file(path):
    if path.endswith('.wav'):
        rate, signal = wavfile.read(path)
        # winsound.PlaySound(path, winsound.SND_FILENAME)
        playsound(path)
        return signal
    else:
        return ([float(line) for line in open(path)])


# x = read_file('./data/file1.txt')
