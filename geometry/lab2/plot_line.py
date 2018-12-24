import time
import sys
import matplotlib.pyplot as pp
import random


def plot_segments(segments):
    # generate ends for the line segments
    xpairs = []
    ypairs = []
    for seg in segments:

        x_end = seg[0]
        print(x_end)
        y_end = seg[1]
        xpairs.append(x_end)
        ypairs.append(y_end)

    '''
        for i in range(100):
        xends = [random.random(), random.random()]
        yends = [random.random(), random.random()]
        xpairs.append(xends)
        ypairs.append(yends)
    '''

    # rebuild ends using none to separate line segments
    xlist = []
    ylist = []
    for xends, yends in zip(xpairs, ypairs):
        xlist.extend(xends)
        #xlist.append(None)
        ylist.extend(yends)
        #ylist.append(None)

    pp.plot(xlist, ylist, 'b-', alpha=0.9)
