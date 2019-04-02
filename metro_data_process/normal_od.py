# -*- coding: utf-8 -*-

# 此代码用于将生成的od_output数据的区域编号统一减1，范围为0-540，另外针对一些非utf-8编码的文件，进行utf-8编码

import os


if __name__ == '__main__':

    fileList = os.listdir("./od_output")
    if not os.path.exists("./od_output_normal"):
        os.makedirs("./od_output_normal")

    for name in fileList:
        if name.find("od") < 0:
            continue
        print(name, " start")
        try:
            with open("./od_output/" + name , 'r') as file:
                with open("./od_output_normal/" + name, 'w', encoding="utf-8") as newfile:
                    for line in file:
                        infor = line.strip('\n').split('\t')
                        infor[3] = str(int(infor[3]) - 1)
                        infor[4] = str(int(infor[4]) - 1)

                        infor = [str(i) for i in infor]
                        str_data = '\t'.join(infor)
                        newfile.write(str_data + '\n')
                
                print("utf-8 ",name, " done")

        except:
            with open("./od_output/" + name , 'r', encoding="gbk") as file:
                with open("./od_output_normal/" + name, 'w', encoding="utf-8") as newfile:
                    for line in file:
                        infor = line.strip('\n').split('\t')
                        infor[3] = str(int(infor[3]) - 1)
                        infor[4] = str(int(infor[4]) - 1)

                        infor = [str(i) for i in infor]
                        str_data = '\t'.join(infor)
                        newfile.write(str_data + '\n')

                print("gbk ",name, " done")



