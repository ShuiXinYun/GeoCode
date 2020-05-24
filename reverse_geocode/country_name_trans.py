import urllib.request
import urllib.parse
import json, csv

# 基于countries.csv, 调用有道api翻译国名生成countries_cn_trans.csv, 生成的文件内容有些需要人为完善


# 调用有道api翻译国家名
def trans(country_name:str):
    content = country_name
    url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    data = dict()
    data['i']=content
    data['from']='AUTO'
    data['to']='AUTO'
    data['smartresult']='dict'
    data['client']='fanyideskweb'
    data['salt']='15601659811655'
    data['sign']='78817b046452f9663a2b36604f220360'
    data['doctype']='json'
    data['version']='2.1'
    data['keyfrom']='fanyi.web'
    data['action']='FY_BY_REALTTIME'
    data=urllib.parse.urlencode(data).encode('utf-8')
    response=urllib.request.urlopen(url,data)
    html=response.read().decode('utf-8')
    target=json.loads(html)
    return target['translateResult'][0][0]['tgt']


# 保存翻译后的国家名字典
def create_data():
    with open('.\\countries.csv', 'r') as in_file:
        with open('.\\countries_cn_trans.csv', 'w', newline='') as out_file:
            csv_in = csv.reader(in_file)
            csv_out = csv.writer(out_file)
            for row in csv_in:
                country_name = str(row[1])
                country_name_cn = trans(country_name)
                print(country_name, country_name_cn)
                row.append(country_name_cn)
                csv_out.writerow(row)


if __name__ == '__main__':
    create_data()