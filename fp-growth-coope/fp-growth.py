#coding:utf-8
# from numpy import *

import json
import os

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode, regionnum):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.regionid = []
        self.regionid.append(str(regionnum))
        self.parent = parentNode      #needs to be updated
        self.children = {} 
        
    def inc(self,numOccur, regionnum):
        self.count += numOccur
        self.regionid.append(str(regionnum))
        
    def disp(self,ind = 1):
        print ' '*ind,self.name,' ',self.count
        for child in self.children.values():
            child.disp(ind+1)

#FP构建函数
#这里的最小支持度对应为共现地区的最小数目
def createTree(dataSet,minSup = 1):
    # print "dataSet: ", dataSet, "\n"
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item,0) + 1#记录每个元素项出现的频度
    # print "headerTable: ", headerTable, "\n";

    for k in headerTable.keys():
        if headerTable[k] < minSup:
            del(headerTable[k])
    #去除最小支持度以下的项
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:#不满足最小值支持度要求的除去
        return None,None
    for k in headerTable:
        headerTable[k] = [headerTable[k],None]
    retTree = treeNode('Null Set',1,None,-1)
    for tranSet,regionid in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(),key = lambda p:p[1],reverse = True)]
            # print "count: ", regionid, "\n"
            updateTree(orderedItems,retTree,headerTable,1, regionid)
    return retTree,headerTable

# 默认后面的count都为1
def updateTree(items, inTree, headerTable, count, regionid):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count, regionid)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree, regionid)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count, regionid)

def updateHeader(nodeToTest, targetNode):   
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

def createInitSet(dataSet):
    # print "origin_data: ", dataSet, "\n"
    retDict = {}
    index = 0
    for trans in dataSet:
        # print trans
        retDict[frozenset(trans)] = index
        index += 1
    # print "retDict: ", retDict, "\n"
    return retDict


def ascendTree(leafNode, prefixPath): #ascends from leaf node to root
    if leafNode.parent != None:
        # print leafNode.regionid
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)
    
def findPrefixPath(basePat, headTable): #treeNode comes from header table
    condPats = {}
    treeNode = headTable[basePat][1]
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        # print "\nend\n"
        if len(prefixPath) > 1: 
            condPats[frozenset(prefixPath[0:])] = treeNode.regionid
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]#(sort header table)
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup)
        if myHead != None:            
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def loadjson(filename):
    with open(filename, 'r') as file:
        data = json.load(file, encoding="utf-8")

        for timeid in range(1):
            timedata = data[str(timeid)]

            fpdata = []
            for item in timedata:
                tmpdata = []
                for key in item:
                    # print key
                    tmpdata.append(key)
                    # print tmpdata
                fpdata.append(tmpdata)

            initSet  = createInitSet(fpdata)
            myFPtree,myHeaderTab = createTree(initSet,3)

            for key in myHeaderTab:
                print key, ": ", findPrefixPath(key,myHeaderTab)

def test():
    #test
    simpDat = loadSimpDat()
    initSet  = createInitSet(simpDat)
    myFPtree,myHeaderTab = createTree(initSet,3)

    for key in myHeaderTab:
        print key, ": ", findPrefixPath(key,myHeaderTab)

def process(data_dir, filename):
    
    if not os.path.exists("./coope"):
        os.makedirs("./coope")
    outputfile = "./coope/coope_" + filename
    with open(data_dir + filename, 'r') as file:
        print filename
        data = json.load(file, encoding="utf-8")
        
        #该文件48个时间段的共现数据
        coope_data = []

        for timeid in range(48):
            timedata = data[str(timeid)]

            # 一个时间片的共现数据
            time_coope_data = {}
            time_coope_data["TimeId"] = str(timeid)
            # fp-growth输入格式处理
            fpdata = []
            for item in timedata:
                if item == None:
                    continue
                tmpdata = []
                for key in item:
                    tmpdata.append(key)
                fpdata.append(tmpdata)

            #fp树构建过程
            initSet  = createInitSet(fpdata)
            myFPtree,myHeaderTab = createTree(initSet,1)

            # 一个时间段的所有frequernt_set
            frequent_set = []
            for key in myHeaderTab:
                single_fre_set = findPrefixPath(key,myHeaderTab)
                
                for item in single_fre_set:
                    desnum = str(len(single_fre_set[item]))
                    sournum = str(len(item))

                    key = ','.join(item)
                    value = ','.join(single_fre_set[item])

                    coopeone = {}
                    coopeone["desnum"] = desnum
                    coopeone["sournum"] = sournum
                    coopeone["source"] = key
                    coopeone["destination"] = value
                    if desnum == "1":
                        continue
                    frequent_set.append(coopeone)
            time_coope_data["frequent_set"] = frequent_set
            coope_data.append(time_coope_data)

        
        with open(outputfile, 'w') as f:
            json_str = json.dumps(coope_data, indent=4)
            f.write(json_str)


if __name__ == '__main__':
    data_dir = "./flow_data/"
    filenamelist = os.listdir(data_dir)
    for filename in filenamelist:
        # print filename
        process(data_dir, filename)








