import json, csv


# 基于geocode, 输出geocode_full 
# geocode格式：latitude, longitude, country_code, city_name
# geocode_full格式: latitude, longitude, 中文国名, city_name

def geocode_full():
    country_name_dict = dict()
    with open('.\\countries_cn.csv', 'r') as f:
        c = csv.reader(f)
        for row in c:
            country_code = str(row[0])
            country_name = str(row[1])
            country_name_dict[country_code] = country_name

    with open('.\\geocode.csv', 'r', encoding='utf-8') as in_file:
        with open('.\\geocode_full.csv', 'w', encoding='utf-8', newline='') as out_file:
            csv_in = csv.reader(in_file)
            csv_out = csv.writer(out_file)
            for row in csv_in:
                country_name = country_name_dict[str(row[2])]
                row[2] = country_name
                csv_out.writerow(row)


if __name__ == '__main__':
    geocode_full()