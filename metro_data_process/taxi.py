import json
import os

dataroot = "./taxi_flow/"
filename = os.listdir(dataroot)

outputpath = "./taxi_flow_output"
if not os.path.exists(outputpath):
    os.makedirs(outputpath)

for name in filename:
    if name.find("day") < 0:
        continue
    print(name, " start")
    with open(dataroot + name, "r") as file:
        data = json.load(file)
        for region in data:
            region["label"] = int(region["label"]) - 1
        
        with open(outputpath + "/" + name, 'w', encoding="utf-8") as newfile:
            json.dump(data, newfile, ensure_ascii=False, indent=4)
    
    print(" end!")

        
        

