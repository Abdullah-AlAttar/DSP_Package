
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


def read_ds_file(path):
    if path.endswith('.wav'):
        rate, signal = wavfile.read(path)
        # winsound.PlaySound(path, winsound.SND_FILENAME)
        playsound(path)
        return dict(zip(range(len(signal)), signal.tolist()))

    f = open(path)
    signal_type = int(f.readline())
    if signal_type == 0:
        is_periodic = int(f.readline())
        num_of_samples = int(f.readline())
        signal = dict()
        for i in f:
            i = i.split()
            signal[int(i[0])] = float(i[1])
        return signal
    elif signal_type == 1:
        is_periodic = int(f.readline())
        num_of_samples = int(f.readline())
        freq, amp, phase = [], [], []
        for i in f:
            i = i.split()
            freq.append(float(i[0]))
            amp.append(float(i[1]))
            phase.append(float(i[2]))
        return freq, amp, phase


def save_ds_file(path, signal, type=0):
    f = open(path, mode='w')
    f.write('0\n')
    f.write('0\n')
    f.write(str(len(signal)) + '\n')
    for s in signal:
        f.write(str(s) + ' ' + str(signal[s]) + '\n')
    f.close()


def save_ds_frequency(path, x_axis, amplitude, phase):
    f = open(path, mode='w')
    f.write('1\n')
    f.write('0\n')
    f.write(str(len(amplitude)) + '\n')

    for i in range(len(x_axis)):
        f.write(str(x_axis[i]) + ' ' + str(amplitude[i]) +
                ' ' + str(phase[i]) + '\n')
    f.close()
