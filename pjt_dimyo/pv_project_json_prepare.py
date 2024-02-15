import json
import time
import geopy.geocoders
from geopy.geocoders import GoogleV3
import certifi
import ssl
import re
import shapely

# Step. addr-coord 파일에서 정보를 읽어와 기본 정보를 생성.
year = 2023
addr_coord_file = 'files/2023_pv_project_address_coord_dict.csv'
addr_coord_dict = dict()

with open(addr_coord_file, 'r') as file:
    line = file.readline()
    while line:
        row = line.replace('\n','').split(',')

        if row[0] not in addr_coord_dict:
            addr_coord_dict[row[0]] = {
                'lat': row[1],
                'lng': row[2]
            }

        line = file.readline()
    file.close()

print(addr_coord_dict)

# Step. 각 Element 에 대하여 Google Geocoder 기반으로 위경도 값을 읽어와 추가 후, csv 로 출력


# import 를 위해 Google storage bucket 에 업로드
