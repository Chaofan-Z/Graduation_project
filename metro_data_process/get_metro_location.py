# -*- coding: utf-8 -*-

import json
import io
import sys

region = {}

def judgeregionid(x, y):
    for item in region:
        if int(item['x']) == int(x) and int(item['y']) == int(y):
            return item['label']
    return -1

location = []
with io.open("./metroStation_infor/车站.csv", 'r') as file:
    next(file)
    for line in file:
        da = line.strip('\n').split(',')
        if da[4] == "" or da[5] =="":
            da[4] = "0"
            da[5] = "0"
        name = da[2].replace(' ', '')
        loc = str(da[3]) + "号线" + str(da[1]) + '\t' + name + '\t' + str(da[4]) + '\t' + str(da[5])
        location.append(loc)
        # print (loc)

#确定站点经纬度
normal = []
anomalies = []
with open("./metroStation_infor/stationLocationGPS.json", "r") as file:
    data = json.load(file)
    # print(len(data))
    for item in location:
        infor = item.strip('\n').split('\t')
        if infor[1] in data:
            itude = data[infor[1]]
            infor.extend(itude)
            normal.append(infor)
        
        else :
            anomalies.append(infor)
    

# 这里从车站.csv删除了严御路这个站,anomalies为空，已经存在metro_station
# for item in normal:
#     item = [str(i) for i in item]
#     str_data = '\t'.join(item)
#     print(str_data)
# for item in anomalies:
#     print(item)

# normal 即为 metro_station
# 1号线莘庄	Xinzhuang	201	771	121.38033486645138	31.112825888258474
# 1号线外环路	Waihuanlu	224	738	121.38856113556504	31.123131584366114


# print (normal)

for item in normal:
    E = float(item[4])
    N = float(item[5])

    x = 745 * (E - 121.31) / 0.53 
    y = 469 * (31.37 - N) / 0.22
    
    item.append(int(x + 0.5))
    item.append(int(y + 0.5))

# for item in normal:
#     item = [str(i) for i in item]
#     str_data = '\t'.join(item)
#     print(str_data)
    



with io.open("./metroStation_infor/lable.json", 'r') as file:
        region = json.load(file)

        new_normal = []
        for item in normal:
            x = int(item[6])
            y = int(item[7])
            
            for item2 in region:
                if int(item2["x"]) == x and int(item2["y"]) == y:
                    # print(1)
                    # 这里根据需求统一将regionid - 1 如果需要重新跑实验，后面生成od的时候那个normal.py减一的操作要省略
                    item.append(int(item2["lable"]) - 1)
                    new_normal.append(item)
                    break

# 此时metro_station 这个文件已经是对应站点的区域划分了，删除掉了没有在选定范围内的站点
for item in new_normal:
    item = [str(i) for i in item]
    str_data = '\t'.join(item)
    print(str_data)
  




    

