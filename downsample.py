from math import ceil
from numpy import array
import matplotlib.pyplot as plt
import datetime


def drop(L, N):
    return [x for i, x in enumerate(L) if i % N == 0]


def downsample(x, y):

    x = array(drop(x, ceil(len(x) / 500000.0)))
    y = array(drop(y, ceil(len(y) / 500000.0)))

    return x, y


if __name__ == "__main__":
    x = range(3, 1800000)
    print 'len x is %g' % (len(x))
    y = range(4, 1800001)
    print 'len y is %g' % (len(y))

    x1, y1  = downsample(x, y)
    print ''
    print 'len x1 is %g' % (len(x))
    print 'len y1 is %g' % (len(y))

    a = 5
    b = 4

    plt.plot(x, y, 'o', label='Original data', markersize=1)
    plt.plot(x1, a * x1 + b, 'r', label='Fitted line')
