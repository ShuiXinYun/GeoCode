from global_land_mask import globe
import numpy as np
import time


#  海陆分离数据生成
def global_land_sea_data_001():
    lon_begin = -180.0
    lon_end = 180.0
    lon_interval = 0.01
    lat_begin = -90.0
    lat_end = 90.0
    lat_interval = 0.01
    t0 = time.time()
    with open('land_sea_0.01deg.dat', 'wb') as f:
        lon_range = [round(lon, 2) for lon in np.arange(lon_begin, lon_end+lon_interval, lon_interval)]
        lat_range = [round(lat, 2) for lat in np.arange(lat_begin, lat_end + lat_interval, lat_interval)]
        lon = list()
        lat = list()
        lon_len = len(lon_range)
        slice_interval = 1000
        slice_begin = 0
        slice_end = slice_interval
        while slice_begin < lon_len:
            if slice_end > lon_len:
                slice_end = lon_len
            for lon_ in lon_range[slice_begin:slice_end]:
                for lat_ in lat_range:
                    lon.append(lon_)
                    lat.append(lat_)
            result = globe.is_land(lat, lon)
            for r in result:
                if r:
                    t = 1
                    result_byte = t.to_bytes(1, byteorder='big')
                    f.write(result_byte)
                else:
                    t = 0
                    result_byte = t.to_bytes(1, byteorder='big')
                    f.write(result_byte)
            lon.clear()
            lat.clear()
            slice_begin += slice_interval
            slice_end += slice_interval
            print("output:{0}/{1}".format(slice_begin, lon_len))
        
    t1 = time.time()
    print("land_sea data output, time cost:", t1-t0)


if __name__ == '__main__':
    global_land_sea_data_001()