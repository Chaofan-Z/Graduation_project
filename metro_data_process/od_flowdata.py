# -*- coding: utf-8 -*-
import os
import io
import sys
import json
import time

emptyData = []

for i in range(541):
    reData = {}
    reData["label"] = i
    reData["item"] = []
    for j in range(48):
        tiData = {}
        tiData["time"] = j
        tiData["flow_in"] = 0
        tiData["flow_out"] = 0
        reData["item"].append(tiData)
    emptyData.append(reData)
    
# 导出来查看下数据格式是否正确
# with open("./flowempty.json", "w") as file:
#     json.dump(emptyData, file, ensure_ascii=False,indent=4)


def odToFlow(filename):
    data = emptyData

    with open(filename, "r") as file:
        for line in file:
            infor = line.strip('\n').split('\t')
            #现寻找regionid(label)再找对应的time
            # emptyData[起/终reid]["item"][起/终tiid]["flow_in"] += 1
            # 要求regionid和timeid都是从0开始，timeid是从0开始的，region需要整体减1
            data[int(infor[3])]["item"][int(infor[6])]["flow_in"] += 1
            data[int(infor[4])]["item"][int(infor[8])]["flow_out"] += 1
    

    filename = os.path.basename(filename)

    if not os.path.exists("./flow_output"):
            os.makedirs("./flow_output")

    outputPath = "./flow_output/"
    with open(outputPath + "flow_" + filename + '.json', "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":

    dataRoot = "./od_output/"
    fileNameList = os.listdir(dataRoot)
    for fileName in fileNameList:
        if fileName.find("od") < 0:
            continue
        print(fileName ," start!")
        odToFlow(dataRoot + fileName)
        print(fileName, " done!")
    
