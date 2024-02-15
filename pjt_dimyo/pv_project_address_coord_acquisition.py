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
input_file_path = 'files/2022_pv_project_origin.txt'
# input_file_path = 'files/2023_pv_developer_origin_sample.txt'
address_coord_dict = dict()

# Step. 각 Element 에 대하여 Google Geocoder 기반으로 위경도 값을 읽어와 추가 후, csv 로 출력
with open('google_develop.key', 'r') as file:
    api_key = file.read().strip()

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geocoder = GoogleV3(api_key=api_key, user_agent='mimi')

with open(input_file_path, 'r') as file:
    line = file.readline()
    while line:
        # 중간에 tap+" 포함된 것들 변경
        line_1 = line.replace('\t"', '').replace('"', '').replace('\n', '')

        row = line.split('\t')

        if row[2] in address_coord_dict:
            pass
        else:
            locCoord = geocoder.geocode(row[2])
            time.sleep(0.1)
            print(f'{row[2]},{locCoord.latitude},{locCoord.longitude}')
            address_coord_dict[row[2]] = 'obtained'

        line = file.readline()
    file.close()