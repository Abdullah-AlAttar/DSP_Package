from EnumsClasses import SinOrCos, TypeOfNormalization
import numpy as np
import math


class SignalGeneration:

    def Signal(self, SizeOfFile=None, A=None, F=None, Fs=None, Theta=None, SinORCos=None):
        NewSignal = []
        for i in range(SizeOfFile):
            if SinORCos == SinOrCos.sin:
                NewSignal.append(
                    A * math.sin((2 * math.pi * (F / Fs) * i) + Theta))
            elif SinORCos == SinOrCos.cos:
                NewSignal.append(
                    A * math.cos((2 * math.pi * (F / Fs) * i) + Theta))
        return NewSignal

    def NormalizeSignal(self, Signal=None, Type=None):
        yValues = [y[1] for y in Signal]
        minimum = np.min(yValues)
        maximum = np.max(yValues)
        NormalizedSignalList = []
        for i in range(len(yValues)):
            if Type == TypeOfNormalization.zeroToOne:
                NormalizedSignalList.append(
                    (yValues[i] - minimum) / (maximum - minimum))
            elif Type == TypeOfNormalization.negativeOneToOne:
                NormalizedSignalList.append(
                    (2 * ((yValues[i]) - minimum) / (maximum - minimum)) - 1)
        return NormalizedSignalList

    def MovingAverage(self, Kernal=None, Signal=None):
        filterSize = (Kernal - 1) / 2
        yValues = [y[1] for y in Signal]
        AveragedSignal = []
        for i in range(int(filterSize)):
            yValues.insert(0, 0)
        for i in range(int(filterSize)):
            yValues.append(0)
        for i in range(len(yValues) - Kernal + 1):
            if Kernal == 3:
                AveragedSignal.append(
                    (yValues[i] + yValues[i + 1] + yValues[i + 2]) / Kernal)
            elif Kernal == 5:
                AveragedSignal.append(
                    (yValues[i] + yValues[i + 1] + yValues[i + 2] + yValues[i + 3] + yValues[i + 4]) / Kernal)
        return AveragedSignal

    def SignalDerivative(self, Signal=None):
        yValues = [y[1] for y in Signal]
        derivativeList = []
        for i in range(len(yValues)):
            if i == 0:
                derivativeList.append(yValues[i])
            else:
                derivativeList.append(yValues[i] - yValues[i - 1])
        return derivativeList

    def RemovingDcComponents(self, Signal=None):
        yValues = [y[1] for y in Signal]
        Average = sum(yValues) / float(len(yValues))
        DC = []
        for i in range(len(yValues)):
            DC.append(yValues[i] - Average)
        return DC
