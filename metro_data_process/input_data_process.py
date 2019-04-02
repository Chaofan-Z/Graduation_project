# -*- coding: utf-8 -*-

import os
import json


if __name__ == '__main__':
    
    data = []
    for i in range(1440):
        a = [0] * 1082
        data.append(a)

    dataRoot = "./metro_flow_output/"
    
    # 修改为taxi时，要改 dataRoot，输出文件名，以及day的判定
    # dataRoot = "./taxi_flow_output/"


    fileNameList = os.listdir(dataRoot)
    for fileName in fileNameList:

        if fileName.find("flow") < 0:
            continue
        print("read ",fileName, "'s data")

        day = int(fileName[-7:-5])
        # day = int(fileName[0:2])

        with open(dataRoot + fileName, "r") as file:
            partData = json.load(file)

            for regionData in partData:
                regionId = int(regionData["label"])

                for regionTimeData in regionData["item"]:
                    timeId = regionTimeData["time"]
                    # 这里设定先flowin后flowout
                    try:
                        data[timeId + (day - 1) * 48][regionId * 2] = regionTimeData["flow_out"]
                        data[timeId + (day - 1) * 48][regionId * 2 + 1] = regionTimeData["flow_out"]

                    except:
                        print(regionId * 2, regionId * 2 + 1, regionId)
                        
        
        print("read ",fileName, "'s data done!")


    if not os.path.exists("./matrix_data/"):
        os.makedirs("./matrix_data/")
    

    with open("./matrix_data/metro.txt", 'w', encoding="utf-8") as file:
        for item in data:
            item = (str(i) for i in item)
            str_data = ' '.join(item)
            file.write(str_data + '\n')
