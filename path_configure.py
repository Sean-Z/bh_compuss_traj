# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd
import time
import sys

def parse():
    datas = []
    totalListData = pd.read_csv('demo.csv')
    totalListDict = totalListData.to_dict('index')
    for i in range(0, len(totalListDict)):
        datas.append(str(totalListDict[i]['centroidx']) + ',' + str(totalListDict[i]['centroidy']))
    return datas


def haha():
    key = 'dd59f093b0555104741aed529fdaffb1'
    doc = open('out.txt', 'w')
    with open(".\\pathfiles1\ReceivedTofile-COM7-2021-01-10_11-54-01.DAT", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            line = line.split(",")
            latitude = str((float(line[2]) - 3900) / 60 + 39)
            longtitude = str((float(line[4]) - 11600) / 60 + 116)
            print(longtitude + "," + latitude, file=doc)
    doc.close()


if __name__ == '__main__':
    i = 0
    count = 0
    df = pd.DataFrame(columns=['location', 'detail'])
    locations = parse()
    for location in locations:
        print(location)
