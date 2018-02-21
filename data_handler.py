
import itertools


class Data:
    def __init__(self):
        self.signals = []

    def apply_operation(self, signal, op):
        if op == 's':
            for s in self.signals:
                for i in range(len(s)):
                    s[i] *= signal
        else:
            for s in self.signals:
                for i in range(min(len(s), len(signal))):
                    if op == '+':
                        s[i] += signal[i]
                    elif op == '-':
                        s[i] -= signal[i]

    def quantize(self, levels):
        flattened_list = list(itertools.chain(*self.signals))
        mi, ma = min(flattened_list), max(flattened_list)
        delta = (ma - mi) / float(levels)

        midpoints = []
        print(levels)
        for i in range(levels):
            midpoints.append(((mi + delta) + mi) / 2.0)
            mi += delta

        for s in self.signals:
            for i in range(len(s)):
                s[i] = self._find_nearset_midpoint(s[i], midpoints)

    def _find_nearset_midpoint(self, signal, midpoints):
        val = 1000000000
        res = None
        for m in midpoints:
            if val > abs(m - signal):
                res = m
                val = abs(m - signal)
        return res
