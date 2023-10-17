import json
import os

from iot.mysql import MysqlClient

iot_db_client = MysqlClient(
    username=os.environ.get("IOT_DB_USERNAME"),
    password=os.environ.get("IOT_DB_PASSWORD"),
    host=os.environ.get("IOT_DB_HOST"),
    port=os.environ.get("IOT_DB_PORT"),
    db_name='rtu_db'
)

# 전체 valid inverter name set 추출
all_ivt_names = iot_db_client.runSelectQuery(
    "SELECT master_model_name FROM `iot-device-db`.supporting_inverters"
).all()

all_ivt_names_set = set()

for ivt_name in all_ivt_names:
    all_ivt_names_set.add(ivt_name.master_model_name)

print(all_ivt_names_set)

# 전체 rtu_v1 models 정보 추출
all_rtu_v1_devices = iot_db_client.runSelectQuery(
    "SELECT serial_number, inverter_map FROM modems"
).all()

# 등록 인버터 명 별 serial 목록담는 맵 생성
per_model_serial_list = dict()

for rtu_v1 in all_rtu_v1_devices:
    serial = rtu_v1[0]
    ivt_model = json.loads(rtu_v1[1])

    for key in ivt_model:
        if key in per_model_serial_list:
            per_model_serial_list[key].append(serial)
        else:
            per_model_serial_list[key] = [serial]

# rtu_v1 등록된 발전소 찾아냄


# 등록 인버터 명 별 serial 에서 valid inverter 명에 포함되지 않는 것 골라서 출력
to_ret = []

for model_name, serial_list in per_model_serial_list.items():
    print(model_name)

    if model_name in all_ivt_names_set:
        print(model_name + '이 있음')
    else:
        print(model_name + '이 없음')

    if model_name not in all_ivt_names_set:
        to_ret.append({
            'invalid_model_name': model_name,
            'rtu_v1_serial_list': serial_list
        })

print(json.dumps(to_ret))




