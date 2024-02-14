import time
import geopy.geocoders
from geopy.geocoders import GoogleV3
import certifi
import ssl
import re
import shapely

# Preprocess. 기본 상수들 정의.
# schema: 'year,name,gwangyeok,biz_reg_num,president,address,locCoords,note,total_capa,total_prj_num,relation'

# Step. 파일에서 정보를 읽어와 기본 정보를 생성.
year = 2023
input_file_path = '../files/2023_pv_developer_origin.txt'
# input_file_path = 'files/2023_pv_developer_origin_sample.txt'
developer_list = []

with open(input_file_path, 'r') as file:
    line = file.readline()
    while line:
        row = line.split('\t')

        developer = {
            "year": year,
            "name": row[1],
            "gwangyeok": row[0],
            "biz_reg_num": row[2] if row[2] != '' else '-',
            "president": row[3].replace(' ', '').replace(',', '/') if row[3] != '' else '-',
            "address": row[4].replace(',', ' ') if row[4] != '' else '-',
            "note": row[5].replace(',', ' ') if row[5] != '' else '-',
            "total_capa": float(re.findall(r'[-+]?[0-9]*\.?[0-9]+', row[6])[0]),
            "total_prj_num": int(re.findall(r'[-+]?[0-9]*\.?[0-9]+', row[8])[0]),
            "relation": row[10] if len(row) == 11 else ''
        }

        developer_list.append(developer)

        line = file.readline()
    file.close()

# Step. 각 Element 에 대하여 Google Geocoder 기반으로 위경도 값을 읽어와 추가 후, csv 로 출력
with open('../google_develop.key', 'r') as file:
    api_key = file.read().strip()

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geocoder = GoogleV3(api_key=api_key, user_agent='mimi')

for item in developer_list:
    if item["address"] != '':
        locCoord = geocoder.geocode(item["address"])

        # schema: 'year,name,gwangyeok,biz_reg_num,president,address,latitude,longitude,note,total_capa,total_prj_num,relation'
        print(f'''{item['year']},{item['name']},{item['gwangyeok']},{item['biz_reg_num']},{item['president']},''' +
              f'''{item['address']},{locCoord.latitude},{locCoord.longitude},{item['note']},{item['total_capa']},{item['total_prj_num']},''' +
              f'''{item['relation']}''')
        time.sleep(0.1)
    else:
        print(f'''{item['year']},{item['name']},{item['gwangyeok']},{item['biz_reg_num']},{item['president']},''' +
              f'''{item['address']},37.5145741,127.1027673,{item['note']},{item['total_capa']},{item['total_prj_num']},''' +
              f'''{item['relation']}''')

# import 를 위해 Google storage bucket 에 업로드
