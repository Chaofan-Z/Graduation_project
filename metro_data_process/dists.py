# -*- coding: utf-8 -*-
import os
import io
import sys
import json
import time
from math import radians, cos, sin, asin, sqrt
from matplotlib import pyplot



nycdist = []
for i in range(862):
    a = [0] * 862
    nycdist.append(a)

with open("./matrix_data/nycdists.txt", 'r') as file:
    index = 0
    for line in file:
        infor = line.strip('\n').split(' ')
        nycdist[index] = infor
        index += 1


nycdistance = []
sunnum = 862*862/2
sum = 0
for i in range(541):
    j = i
    while j < 541:
        nycdistance.append(float(nycdist[i][j]))
        sum += float(nycdist[i][j])
        j += 1

print(sum / sunnum)

for item in nycdistance:
        print (item)

pyplot.hist(nycdistance,100)
pyplot.xlim(0.0,60000)
pyplot.show()

