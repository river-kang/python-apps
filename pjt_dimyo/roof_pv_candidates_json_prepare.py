import json

gwangyeok_set = ['강원', '경상북도', '경상남도', '충청북도', '충청남도', '전라북도', '전라남도',
                 '경기', '서울', '부산', '대전', '광주', '울산', '대구']

gwangyeok_dict = dict()
gwangyeok_dict['강원'] = '강원'
gwangyeok_dict['경상북도'] = '경북'
gwangyeok_dict['경상남도'] = '경남'
gwangyeok_dict['충청북도'] = '충북'
gwangyeok_dict['충청남도'] = '충남'
gwangyeok_dict['전라북도'] = '전북'
gwangyeok_dict['전라남도'] = '전남'
gwangyeok_dict['경기'] = '경기'
gwangyeok_dict['서울'] = '서울'
gwangyeok_dict['부산'] = '부산'
gwangyeok_dict['대전'] = '대전'
gwangyeok_dict['광주'] = '광주'
gwangyeok_dict['울산'] = '울산'
gwangyeok_dict['대구'] = '대구'

file_output = open('files/roof_pv_candidates_data.json', 'w')

with open('files/roof_pv_candidates_origin.txt', 'r') as file:
    line = file.readline()
    while line:
        for gwangyeok in gwangyeok_set:
            if gwangyeok in line:
                rows = line.split("\t")
                # print(f'{gwangyeok} - {line}')
                roof_pv_candidate = {
                    'gwangyeok': gwangyeok_dict[gwangyeok],
                    'address': rows[0],
                    'latitude': rows[2],
                    'longitude': rows[1],
                    'capacity': rows[3],
                    'company': rows[4],
                    'branch': rows[5]
                }

                file_output.write(json.dumps(roof_pv_candidate, ensure_ascii=False))
                file_output.write('\n')
                break
            else:
                continue
        line = file.readline()

file_output.close()

