import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import random

__data = None


#  导入海陆分离数据, 存入__data数组
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


# 使用台湾附近的区域进行测试
def test_land_sea():
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.set_global()
    ax.coastlines(resolution='10m')

    taiwan_lat_lon_range = (21.7, 25.35, 119.301, 124.575)
    for i in range(10000):
        lat = (random.random())*3.65 + 21.7
        lon = (random.random())*5.274 + 119.301
        index = land_sea_index(lat, lon)
        if int(__data[index]) == 0:  # 0为海洋
            plt.plot(lon, lat, 'bo', transform=ccrs.PlateCarree(), markersize=3)
        elif int(__data[index]) == 1:  # 1为陆地
            plt.plot(lon, lat, 'r^', transform=ccrs.PlateCarree(), markersize=4)
    ax.set_extent((taiwan_lat_lon_range[2], taiwan_lat_lon_range[3], taiwan_lat_lon_range[0], taiwan_lat_lon_range[1]))
    plt.show()


if __name__ == '__main__':
    load_land_sea_data('land_sea_0.01deg.dat')
    test_land_sea()