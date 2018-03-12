
import itertools
import sys
import math
import numpy as np


class Data:
    def __init__(self):
        self.signals = []
        self.frequency = None

    def apply_operation(self, signal, op):

        if op == 's':
            for s in self.signals:
                for i in s:
                    s[i] *= signal
        else:
            for s in self.signals:
                if op == '+':
                    for idx in set(s) & set(signal):
                        s[idx] += signal[idx]
                elif op == '-':
                    for idx in set(s) & set(signal):
                        s[idx] -= signal[idx]
                for idx in set(signal) - set(s):
                    s[idx] = signal[idx]

    def quantize(self, levels):

        mi, ma = sys.maxsize, -sys.maxsize
        for s in self.signals:
            mi = min(mi, min(s.values()))
            ma = max(ma, max(s.values()))

        delta = (ma - mi) / float(levels)

        midpoints = []
        print(levels)
        for i in range(levels):
            midpoints.append(((mi + delta) + mi) / 2.0)
            mi += delta
        sample_error = []

        for s in self.signals:
            for i in s:
                new_val = self._find_nearset_midpoint(s[i], midpoints)
                sample_error.append(format(new_val - s[i], '.3f'))
                s[i] = new_val
        # bits_num = math.log2(levels)
        encoding = [bin((i + 1) % (levels))[2:] for i in range(levels)]
        return encoding, sample_error

    def _find_nearset_midpoint(self, signal, midpoints):
        val = sys.maxsize
        res = None
        for m in midpoints:
            if val > abs(m - signal):
                res = m
                val = abs(m - signal)
        return res

    def dft(self, s, inverse=False):
        np.set_printoptions(suppress=True)
        s = np.array(s)
        N = s.shape[0]
        n, k = np.arange(N), np.arange(N).reshape((N, 1))
        jj = np.complex(0 + 2j) if inverse else np.complex(0 - 2j)
        M = np.exp(jj * np.pi * k * n / N)
        res = (np.dot(M, s) / N) if inverse else np.dot(M, s)
        amp = np.sqrt(np.square(res.real) + np.square(res.imag))
        # phase = (np.arctan(res.imag / res.real))
        phase = np.angle(res)
        return res if inverse else (res, amp, phase)

    def generate_signal(self, signal_type='sin', n=100, A=1, theta=0, F=1, Fs=1):
        self.signals.clear()
        if signal_type == 'sin':
            res = [A * np.sin(2 * np.pi * (F / Fs) * i + theta)
                   for i in range(n)]
        else:
            res = [A * np.cos(2 * np.pi * (F / Fs) * i + theta)
                   for i in range(n)]
        self.signals.append(dict(zip(range(len(res)), res)))

# data =  Data()
# data.generate_signal('sin',n=100,A=1)
