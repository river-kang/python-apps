import csv
import json
import os
import io
import csv

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
to_json = []
to_csv = [
    ["rtu_v1_serial", "invalid_model_name"]
]

for model_name, serial_list in per_model_serial_list.items():
    if model_name not in all_ivt_names_set:
        to_json.append({
            'invalid_model_name': model_name,
            'rtu_v1_serial_list': serial_list
        })

        for serial in serial_list:
            to_csv.append([
                serial, model_name
            ])

print(json.dumps(to_json))

# 엑셀 확인 용이하게 csv 로도 출력

# Use StringIO to capture the CSV output
output = io.StringIO()
writer = csv.writer(output)

# Write data to the StringIO object
writer.writerows(to_csv)

# Move the cursor to the beginning of the StringIO object
output.seek(0)

# Print the content
print(output.getvalue())

# Optionally, close the StringIO object
output.close()