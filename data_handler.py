
import itertools
import sys


class Data:
    def __init__(self):
        self.signals = []

    def apply_operation(self, signal, op):
        # if op == 's':
        #     for s in self.signals:
        #         for i in range(len(s)):
        #             s[i] *= signal
        # else:
        #     for s in self.signals:
        #         for i in range(min(len(s), len(signal))):
        #             if op == '+':
        #                 s[i] += signal[i]
        #             elif op == '-':
        #                 s[i] -= signal[i]
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

        for s in self.signals:
            for i in s:
                s[i] = self._find_nearset_midpoint(s[i], midpoints)

    def _find_nearset_midpoint(self, signal, midpoints):
        val = sys.maxsize
        res = None
        for m in midpoints:
            if val > abs(m - signal):
                res = m
                val = abs(m - signal)
        return res
