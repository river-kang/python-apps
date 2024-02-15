import json
import time
import geopy.geocoders
from geopy.geocoders import GoogleV3
import certifi
import ssl
import re
import shapely

# Step. addr-coord 파일에서 정보를 읽어와 기본 정보를 생성.
year = 2022
addr_coord_file = f'files/{year}_pv_project_address_coord_dict.csv'
addr_coord_dict = dict()

with open(addr_coord_file, 'r') as file:
    line = file.readline()
    while line:
        row = line.replace('\n','').split(',')

        if row[0] not in addr_coord_dict:
            addr_coord_dict[row[0]] = {
                'lat': row[1],
                'lng': row[2],
                'index': 1,
                'total': 0
            }

        line = file.readline()
    file.close()

# Step. BigQuery upload 용 json output 생성
project_file_path = f'files/{year}_pv_project_origin.txt'
with open(project_file_path, 'r') as file:
    line = file.readline()
    while line:
        row = line.replace('\n', '').split('\t')

        # if row[9] != '':    # 사업장 면적은 사업 부지 별로 대표로 존재하는게 기본이나, 그렇지 못할 경우 'area' 가 존재하지 않음.
        #     addr_coord_dict[row[2]]['area'] = re.findall(r'[-+]?[0-9]*\.?[0-9]+', row[9])[0]

        if row[8] != '' and row[8] != '미상':
            addr_coord_dict[row[2]]['capa'] = float(row[8])

        addr_coord_dict[row[2]]['total'] = addr_coord_dict[row[2]]['total'] + 1
        line = file.readline()
    file.close()

output_file_path = f'files/{year}_pv_project_data.json'

outpuf_file = open(output_file_path, 'w')

with open(project_file_path, 'r') as file:
    line = file.readline()
    while line:
        row = line.replace('\n', '').split('\t')
        item = {
            'env_compl_date': row[3].replace('/','-'),
            'gwangyeok': row[0],
            'gicho': row[1],
            'gubun': row[2],
            'index': addr_coord_dict[row[2]]['index'],
            'latitude': float(addr_coord_dict[row[2]]['lat']),
            'longitude': float(addr_coord_dict[row[2]]['lng']),
            'biz_owner': row[4],
            'president': row[5],
            'location': row[6],
            'plant_name': row[7],
            #  'capacity': float(row[8]) if row[8] != '' else None,
            'capacity': addr_coord_dict[row[2]]['capa'] / addr_coord_dict[row[2]]['total'] if row[8] == '' or row[8] == '미상' else float(row[8]),
            'area_size': int(addr_coord_dict[row[2]]['area']) if 'area' in addr_coord_dict[row[2]] else None,
            'developer': row[9]
        }

        addr_coord_dict[row[2]]['index'] = addr_coord_dict[row[2]]['index'] + 1
        outpuf_file.write(json.dumps(item, ensure_ascii=False) + '\n')
        line = file.readline()
    file.close()

outpuf_file.close()

# import 를 위해 Google storage bucket 에 업로드
