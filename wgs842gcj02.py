import json
import urllib
import math
import csv
import numpy
from numpy.core import double

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方

def substring(lng,lat):
#转为数值类型
    tmp_x = []
    tmp_y = []

    for n in lng:
        tmp_x.append(float(n))
    lng = tmp_x;
    for m in lat:
        tmp_y.append(float(m))
    lat = tmp_y;
    return lng,lat

def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret

def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    resx = []
    resy = []

    lng,lat=substring(lng,lat)
    for i in range(len(lng)):
        dlat = _transformlat(lng[i] - 105.0, lat[i] - 35.0)
        dlng = _transformlng(lng[i] - 105.0, lat[i] - 35.0)
        radlat = lat[i] / 180.0 * pi
        magic = math.sin(radlat)
        magic = 1 - ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
        dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
        mglat = lat[i] + dlat
        mglng = lng[i] + dlng
        resx.append(mglat)
        resy.append(mglng)
    return resx, resy

if __name__ == '__main__':
    doc = open('out.txt', 'w')
    long = []
    lati = []
    with open(".\\pathfiles2\ReceivedTofile-COM7-2021-01-10_18-07-40.DAT", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            line = line.split(",")
            latitude = str((float(line[2]) - 3900) / 60 + 39)
            longtitude = str((float(line[4]) - 11600) / 60 + 116)
            long.append(longtitude)
            lati.append(latitude)
            print(longtitude + "," + latitude, file=doc)
    doc.close()
    result = wgs84_to_gcj02(long,lati)
    k = 1
    f = open('geo_out.csv', 'w', encoding='utf-8',newline="")
    csv_writer = csv.writer(f)
    for i in range(len(result[0])):
        csv_writer.writerow([str(result[1][i]),str(result[0][i]),k])
        k = k + 1
    f.close()
