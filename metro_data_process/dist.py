# -*- coding: utf-8 -*-
import os
import io
import sys
import json
import time
from math import radians, cos, sin, asin, sqrt
from matplotlib import pyplot

#公式计算两点间距离（m）

def geodistance(lng1,lat1,lng2,lat2):

    #lng1,lat1,lng2,lat2 = (120.12802999999997,30.28708,115.86572000000001,28.7427)
    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)]) # 经纬度转换成弧度
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2 
    distance=2*asin(sqrt(a))*6371*1000 # 地球平均半径，6371km
    distance=round(distance,3)

    return distance

class metro_station:
    E = 0.0
    N = 0.0
    def __init__(self, e, n):
        self.E = e
        self.N = n

dist = []
for i in range(541):
    a = [0] * 541
    dist.append(a)


station = []
for i in range(541):
    a = metro_station(0.0, 0.0)
    station.append(a)

with open("./metroStation_infor/center.json", "r") as file:
    data = json.load(file)

    for item in data:
        station[int(item["label"]) - 1].E = 0.53 * int(item["x"]) / 745 + 121.31
        station[int(item["label"]) - 1].N = 0.22 * int(item["y"]) / 469 + 31.71


for i in range(541):
    for j in range(541):
        dist[i][j] = geodistance(station[i].E, station[i].N, station[j].E, station[j].N)

distance = []
sunnum = 270*541 - 541
sum = 0
for i in range(541):
    j = i
    while j < 541:
        distance.append(dist[i][j])
        sum += dist[i][j]
        j += 1

        
print (sum / sunnum)


with open("./matrix_data/dist.txt", 'w', encoding="utf-8") as file:
    for item in dist:
        item = (str(i) for i in item)
        str_da = ' '.join(item)

        file.write(str_da + '\n')

pyplot.hist(distance,100)
pyplot.xlabel('lenth')
pyplot.xlim(0.0,60000)
pyplot.show()


            