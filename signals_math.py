import numpy as np


def fft(s):
    s = np.array(s)
    N = s.shape[0]
    if N <= 1:
        return s

    even = fft(s[::2])
    odd = fft(s[1::2])

    t = np.exp(np.complex(-2j) * np.pi * np.arange(N // 2) / N)

    return np.concatenate((even + t * odd, 
                           even - t * odd))


def ifft(s):
    return fft(s.conjugate()).conjugate()/s.shape[0]


def fft_convolve(x, h):
    size = len(x) + len(h) - 1

    fsize = 1 << (size - 1).bit_length()
    x = np.append(x, np.zeros(fsize - len(x)))
    h = np.append(h, np.zeros(fsize - len(h)))
    x_fft = fft(x)
    h_fft = fft(h)

    return ifft(x_fft * h_fft).real[:size]


def convolve(x, h):
    res = np.zeros(len(x) + len(h) - 1)

    for i in range(len(x)):
        for j in range(len(h)):
            res[i + j] = res[i + j] + x[i] * h[j]

    return res


b = np.array([1, 1, 1, 1])
a = np.array([6, 5, 4, 3, 2, 1])

print(np.convolve(a, b))
print(convolve(a, b))
print(fft_convolve(a, b))

# print(np.fft.fft(a))
# print(ifft(fft(a)))
