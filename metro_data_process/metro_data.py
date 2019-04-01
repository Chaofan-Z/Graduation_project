# -*- coding: utf-8 -*-
import os
import io
import sys
import json
import time


def maketimeslace(timestamp):
    
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%H:%M", timeArray)
    h = int(str(otherStyleTime).split(':')[0])
    m = int(str(otherStyleTime).split(':')[1])
    return str(h*2 + m//30)

# 处理地铁站点的区域划分
metro_id = {}
with open("./metro_station", 'r') as file:
    for line in file:
        infor = line.strip('\n').split('\t')
        metro_id[infor[0]] = infor[8]



data = {} #处理csv存的dict，每读取一个csv后都会增加很多，然后处理删除掉一些信息生成新的信息得到res_data

dataroot = "./data/"
filenamelist = os.listdir(dataroot)

for inputdata in filenamelist:
    if inputdata.find("csv") < 0 :
        continue
    print (inputdata)
    with io.open(dataroot + inputdata, encoding = "gbk") as file:
        id = set() #用来判断是否第一次出现该id，在dict中判断时间n，set时间1
        index = 0
        for line in file:
            index += 1
            if index%1000000 == 0:
                print(index)
            line = line.strip('\n').split(',')
            strtime = line[1] + " " + line[2]
            timeArray = time.strptime(strtime, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            one_outdata = []
            one_outdata.append(timeStamp)
            one_outdata.append(line[3])
            one_outdata.append(line[5])
            if line[0] in id:
                data[line[0]].append(one_outdata)
            else:
                data[line[0]] = []
                data[line[0]].append(one_outdata)
                id.add(line[0])

    # data = data.encode("utf-8")
    
    # with open("./1.json","w") as f:
    #     json.dump(data,f,ensure_ascii=False)
    # 此时的data是读取当前文件后的信息，每次读取一个都对data当中id中的出行信息进行一次排序，根据时间戳排序，
    # 然后根据严重起始 0 终止不等于0来计算一条，然后将这两个信息在id对应list中删除
    # id start_loc end_loc start_time s_timeslice end_time e_timeslice price

    res_data = [] #处理dict得到的一条条od数据，每个文件单独生成吧
    for item in data:
        thedata = sorted(data[item],key=(lambda x:x[0]))
        i = 0

        res_index = 0
        while i < len(thedata):
            if i+1 >= len(thedata):
                break
            
            one = thedata[i]
            two = thedata[i+1]

            res = []
            if int(one[0]) < int(two[0]) and one[2] == "0.00" and two[2] != "0.00":
                
                res.append(item) #id
                res.append(one[1]) #起点
                res.append(two[1]) #终点
                # 存在起点终点不在选定范围的数据，不加入res_Data但还是要配对删除的
                if one[1] in metro_id and two[1] in metro_id:
                    res.append(metro_id[one[1]])
                    res.append(metro_id[two[1]])
                    res.append(one[0])
                    res.append(maketimeslace(one[0]))
                    res.append(two[0])
                    res.append(maketimeslace(two[0]))
                    res.append(one[2])
                    res.append(two[2])
                    res_data.append(res)

                    res_index += 1
                    if res_index%1000 == 0:
                        print("已经写入：", res_index) 
                # print(res)
                del thedata[i]
                del thedata[i]
            else :
                i += 1

        data[item] = thedata

    # data每次读取新的文件都会进行更新

    if not os.path.exists("./output"):
        os.makedirs("./output")
    outfile = "./output/od_" + inputdata[:-4]

    with open(outfile, 'a+') as file:
        for item in res_data:
            item = [str(i) for i in item]
            str_data = '\t'.join(item)
            file.write(str_data)

    print(outfile, "写入完成")
    # with open(outfile, 'w') as file:
    #     sum_oneday_data = ""
    #     for item in res_data:
    #         item = [str(i) for i in item]
    #         str_data = '\t'.join(item)
    #         # print (str_data)
    #         sum_oneday_data = sum_oneday_data + str_data + '\n'
            
    #     file.write(sum_oneday_data.strip('\n'))
