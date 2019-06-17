
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline
ip_record = {}


def readfile(FILENAME='record.log'):
    with open(FILENAME) as f:
        lines = f.readlines()

    for line in lines:
        # print line
        ip, dif = line.split(' ')
        # print ip, dif
        ip_record.setdefault(ip, [])
        ip_record[ip].append(float(dif))


def draw():
    for k, v in ip_record.items():
        print k, v
        x = range(1, len(v) + 1)
        plt.plot(x, v, label=k)

    plt.xlabel('serial number')
    plt.ylabel('time')
    plt.legend()
    plt.show()



if __name__ == '__main__':
    readfile()
    draw()
    # print ip_record
