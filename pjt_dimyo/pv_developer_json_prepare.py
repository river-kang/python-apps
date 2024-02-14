import json
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
input_file_path = 'files/2022_pv_developer_origin.txt'
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
            "biz_reg_num": row[2],
            "president": row[3].replace(' ', ''),
            "address": row[4],
            "note": row[5],
            "total_capa": float(re.findall(r'[-+]?[0-9]*\.?[0-9]+', row[6])[0]),
            "total_prj_num": int(re.findall(r'[-+]?[0-9]*\.?[0-9]+', row[8])[0]),
            "relation": row[10] if len(row) == 11 else ''
        }

        developer_list.append(developer)

        line = file.readline()
    file.close()

# Step. 각 Element 에 대하여 Google Geocoder 기반으로 위경도 값을 읽어와 추가 후, csv 로 출력
with open('google_develop.key', 'r') as file:
    api_key = file.read().strip()

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geocoder = GoogleV3(api_key=api_key, user_agent='mimi')

for item in developer_list:
    if item["address"] != '':
        locCoord = geocoder.geocode(item["address"])
        item['latitude'] = locCoord.latitude
        item['longitude'] = locCoord.longitude
        print(json.dumps(item, ensure_ascii=False))
        time.sleep(0.1)
    else:
        item['latitude'] = 37.5145741
        item['longitude'] = 127.1027673
        print(json.dumps(item, ensure_ascii=False))



# import 를 위해 Google storage bucket 에 업로드
