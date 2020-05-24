import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import time
from geopy.distance import geodesic
import math
import numpy as np


__data = None


#  导入海陆分离数据
def load_land_sea_data(file_path:str):
    global __data
    with open(file_path, 'rb') as f:
        __data = f.read()
    print("land sea data size:{0}".format(len(__data)))


#  依据经纬度获取海陆分离数组的index
def land_sea_index(lat:float, lon:float):
    lat = round(lat, 2)
    lon = round(lon, 2)
    index = int(((lon+180.0)/0.01)*(180.01/0.01) +(lat+90.0)/0.01)
    return index


#  依据两点的经纬度计算两点之间的距离，返回值单位为km
def distance_from_lat_lon(lat1, lon1, lat2, lon2):
    t1 = (lat1, lon1)
    t2 = (lat2, lon2)
    return geodesic(t1, t2).kilometers


#  检查某一海洋点是否为海岸线,dist为距离阈值，单位km
def check_sea_coastline(lat, lon , dist:float):
    lat_range = dist/110.8
    lon_range = dist/(111.31949*math.cos(math.fabs(lat)/180.0*math.pi))
    lat_begin = lat - lat_range
    lat_end = lat + lat_range
    lon_begin = lon - lon_range
    lon_end = lon + lon_range
    if lat_begin < -90.0:
        lat_begin = -90.0
    if lat_end > 90.0:
        lat_end = 90.0
    if lon_begin < -180.0:
        lon_begin = -180.0
    if lon_end > 180.0:
        lon_end = 180.0
    for lat_ in np.arange(lat_begin, lat_end, 0.01):
        for lon_ in np.arange(lon_begin, lon_end, 0.01):
            index_ = land_sea_index(lat_, lon_)
            if __data[index_] == 1 and distance_from_lat_lon(lat_, lon_, lat, lon) <= dist:
                return True
    return False


#  检查某一陆地点是否为海岸线,若是则返回true, dist为距离阈值，单位km
def check_land_coastline(lat, lon , dist:float):
    lat_range = dist/110.8
    lon_range = dist/(111.31949*math.cos(math.fabs(lat)/180.0*math.pi))
    lat_begin = lat - lat_range
    lat_end = lat + lat_range
    lon_begin = lon - lon_range
    lon_end = lon + lon_range
    if lat_begin < -90.0:
        lat_begin = -90.0
    if lat_end > 90.0:
        lat_end = 90.0
    if lon_begin < -180.0:
        lon_begin = -180.0
    if lon_end > 180.0:
        lon_end = 180.0
    for lat_ in np.arange(lat_begin, lat_end, 0.01):
        for lon_ in np.arange(lon_begin, lon_end, 0.01):
            index_ = land_sea_index(lat_, lon_)
            if __data[index_] == 1 and distance_from_lat_lon(lat_, lon_, lat, lon) <= dist:
                return True
    return False


def test_coastline():
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.set_global()
    ax.coastlines(resolution='10m')
    region_lat_lon_range = (21.7, 25.35, 119.301, 124.575)
    lat_begin = region_lat_lon_range[0]
    lat_end = region_lat_lon_range[1]
    lon_begin = region_lat_lon_range[2]
    lon_end = region_lat_lon_range[3]
    t0 = time.time()
    for lat in np.arange(lat_begin, lat_end, 0.01):
        for lon in np.arange(lon_begin, lon_end, 0.01):
            index_ = land_sea_index(lat, lon)
            if int(__data[index_]) == 0 and check_sea_coastline(lat, lon, 5.0):
                plt.plot(lon, lat, 'b.', transform=ccrs.PlateCarree())
    t1 = time.time()
    print("coastline taiwan time cost:{0}".format(t1-t0))
    ax.set_extent((region_lat_lon_range[2], region_lat_lon_range[3], region_lat_lon_range[0], region_lat_lon_range[1]))
    plt.show()


if __name__ == '__main__':
    load_land_sea_data('land_sea_0.01deg.dat')
    test_coastline()