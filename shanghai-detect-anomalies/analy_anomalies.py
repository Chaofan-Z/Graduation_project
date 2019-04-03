# -*- encoding: utf-8 -*-
'''
@File    :   analy_anomalies.py
@Time    :   2019/04/03 09:10:32
@Author  :   Zhengchaofan 
@Contact :   zhengcfwork@gmail.com
@Desc    :   分析生成的anomaly.txt
'''
import os
import json
import numpy as np
import pandas as pd
 
if __name__ == '__main__':
    anomalies = "./matrix_data/anomalies.txt"

    # data = np.loadtxt(anomalies)

    data = []
    with open(anomalies, 'r') as file:
        for line in file:
            infor = line.strip('\n').split(' ')
            # infor = (float(i) for i in infor)
            # print(infor)
            data.append(infor)
    # print(data)
    for i in range(1440):
        for j in range(541):
            
            res = float(data[i][j])
            if res == 0.0:
                # print(i, j, data[i][j])
                continue
            
            print(i, j, res)
   
            
