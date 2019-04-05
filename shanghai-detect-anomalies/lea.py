# -*- encoding: utf-8 -*-
'''
@File    :   shanghai_real.py
@Time    :   2019/04/03 14:47:15
@Author  :   Zhengchaofan 
@Contact :   zhengcfwork@gmail.com
@Desc    :   None
'''
import os
import json 
from datetime import datetime, timedelta
import numpy as np
from sklearn.svm import OneClassSVM

from util import *


#dataRoot = 'path_for_data'
dataRoot = "./matrix_data/"

tmpoutput = "./tmp_output/"

data = np.loadtxt(dataRoot + 'taximetro.txt')
dists = np.loadtxt(dataRoot + 'dist.txt')

nR = 541 # number of regions

# todo: 数据源不该有这么多啊
nS = 4 # number of data sources
MPS = 30 # minutes per time slot
nT = data.shape[0] # nummber of time slots

print(data.shape)
print(dists.shape)
print(nT) # 16848

stDT = datetime(2015,4,1,0,0,0)

# Params for algorithm
alpha = 0.01
beta = 0.05
nDailyAnomaly_int = int(60 / MPS * 24 * nR * alpha)
nDailyAnomaly_r = int(60 / MPS * 24 * nR * beta)

print("int, r" ,nDailyAnomaly_int, nDailyAnomaly_r)

t_delta = 2
corrThres = 0.95
lCorr = 60 * 24 * 7 // MPS  # use one week data for calculating pearson correlation 

print("lCorr:", lCorr)
# todo: 800需要改 nearby的距离
R = 1200
# todo: 这个参数什么意思
nNearPart = 2


mNear = np.identity(nR) # nR长度的单位矩阵
mNear = np.concatenate((mNear, (dists > 0) & (dists <= R)))  # axis = 0横轴，axis = 1 纵轴，默认为0
sMNear = np.repeat(mNear.sum(axis=1), nS*t_delta) 
mNearTile = np.tile(mNear, (1, nS*t_delta))


score_ind = np.zeros((nT, nR*nS)) # nT时间片总个数
score_r = np.zeros((nT, nR)) + 100
score_int = np.zeros((nT, nR)) + 100
anomalies = np.zeros((nT, nR))

# ?????
dVector = (t_delta - 1 + nNearPart) * nS


model_r = OneClassSVM(kernel="rbf", nu=0.1)
model_int = OneClassSVM(kernel="rbf", nu=0.1)
train_r = np.zeros((0, nS))
train_int = np.zeros((0, dVector))

# ???
print("train_r", train_r.shape)
print("train_int", train_int.shape)


tsTrain = 60 * 24 * 7 // MPS #一周的 336
nTrain = tsTrain * nR


detect_st = (datetime(2015,4,29) - stDT).days * 24 * 60 // MPS  # detect anomamlie  #1344
ed = (datetime(2015,4,30) - stDT).days * 24 * 60 // MPS  # 1392

# ??? 看不懂
st = max(detect_st - tsTrain, lCorr)

print(tsTrain ,detect_st, ed, st ) # 336 1344 1392 1008

# detect_st = (datetime(2014,11,27) - stDT).days * 24 * 60 // MPS  # detect anomamlies in 2014-11-27
# ed = (datetime(2014,11,28) - stDT).days * 24 * 60 // MPS



trained = False
p1 = np.einsum('ij,ik->kj', data[(st-lCorr):st,:], data[(st-lCorr):st,:])

print(p1.shape)
np.savetxt(tmpoutput + "./sh/p1.txt", p1, fmt="%d")



# for ts in range(st, ed):
#     print ("ts:", ts)

#     print('\r' + str(ts), end='')

#     # update pearson correlation
#     pp = np.nan_to_num(pairPearson(data[(ts-lCorr):ts,:], data[(ts-lCorr):ts,:], p1))
#     p1 = p1 + data[ts,:] * data[ts,:][:,None]
#     p1 = p1 - data[ts-lCorr,:] * data[ts-lCorr,:][:,None] 
#     pp_new = np.nan_to_num(pairPearson(data[(ts-lCorr+1):(ts+1),:], data[(ts-lCorr+1):(ts+1),:], p1))  

#     pp_diff = pp - pp_new
#     pp_diff[np.where(np.logical_or(pp < corrThres, pp_diff < 0))] = 0
#     pp_diff = pp_diff * lCorr
#     pp_tmp = np.array(pp)
#     pp_tmp[np.where(pp < corrThres)] = 0

#     # calculate individual anomaly score    
#     scaledData = ((data[:(ts+1),:] - data[:(ts+1),:].mean(0)) / data[:(ts+1),:].std(0))[-1]
#     weightedAvg = np.nan_to_num(np.sum(pp_tmp * np.tile(scaledData, (scaledData.shape[0], 1)), axis = 1) / np.sum(pp_tmp, axis=1))
#     sign = ((scaledData > weightedAvg).astype(int) - 0.5) * 2
#     score_ind[ts,:] = sign * np.nan_to_num(np.sum(pp_tmp * pp_diff, axis=1) / np.sum(pp_tmp, axis=1))
    
#     tmpX = (mNearTile * score_ind[(ts-t_delta+1):(ts+1),:].ravel()).reshape((-1, nR)).sum(axis=1)
#     tmpX = np.nan_to_num(tmpX / sMNear)
#     tmpX = tmpX.reshape(nNearPart, nR, t_delta, nS).transpose([1,2,0,3]).reshape((nR, -1))
#     tmpX = np.c_[tmpX[:,-nS*nNearPart:], tmpX[:,:-nS*nNearPart].reshape((nR,t_delta-1,nNearPart,nS))[:,:,0,:].reshape((nR,-1))]
#     x_r = np.array(tmpX[:,0:nS])
#     x_int = np.array(tmpX)
    
#     train_r = np.r_[train_r, x_r][-nTrain:,:]
#     train_int = np.r_[train_int, x_int][-nTrain:,:]

#     if ts > detect_st:
#         if ts % (60 // MPS * 24) == 0 or not trained:
#             model_r.fit(train_r)
#             model_int.fit(train_int)
#             trained = True
        
#         score_r[ts,:] = model_r.decision_function(x_r).flatten()
#         score_int[ts,:] = model_int.decision_function(x_int).flatten()
#         argsort_r = score_r[(ts-60*24//MPS+1):(ts+1),:].flatten().argsort()
#         argsort_int = score_int[(ts-60*24//MPS+1):(ts+1),:].flatten().argsort()
        
#         selected_int = argsort_int[np.where(np.in1d(argsort_int, argsort_r[0:nDailyAnomaly_r]))[0]][0:nDailyAnomaly_int]
#         iAnomalies = selected_int[(selected_int // nR) == (60 * 24 // MPS - 1)] % nR
#         iAnomalies = iAnomalies[score_int[ts,iAnomalies] != 100]
#         anomalies[ts,iAnomalies] = 1

# np.savetxt(dataRoot + "anomalies2.txt", anomalies, fmt="%d") # detected anomalies








def test():
    dists = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    R = 3
    nR = 4
    print((dists > 0) & (dists <= R))
    mNear = np.identity(nR)
    mNear = np.concatenate((mNear, (dists > 0) & (dists <= R)))  # axis = 0横轴，axis = 1 纵轴，默认为0 ,上下拼接起来
    print("mNear",mNear)
    print("mNear sum : ",mNear.sum(axis=1)) # 压缩纵轴，
    sMNear = np.repeat(mNear.sum(axis=1), nS*t_delta) # 每个元素重复了八次。。。
    print("sMNear:",sMNear)
    mNearTile = np.tile(mNear, (1, nS*t_delta)) # 横向整体重复了八次
    print("mNearTile",mNearTile)

    p1 = np.einsum('ij,ik->kj', data[(st-lCorr):st,:], data[(st-lCorr):st,:])
