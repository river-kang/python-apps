import traceback

from google.cloud import storage, bigquery
import random
import string
import os

random_str = ''.join(random.sample(string.ascii_letters, 10))

output_file_name = f'output-{random_str}.csv'

output_file = open(f'files/{output_file_name}', 'w', encoding='utf-8')

# EPSIS 로 부터 데이터를 얻은 날짜 입니다.
get_date = '2024-02-01'
lines_to_write = []

with open('files/HOME_발전설비_발전기별_20240201.csv', 'r', encoding='euc-kr') as file:
    line = file.readline()
    while line:
        lines_to_write.append(line)
        line = file.readline()

    # last row 는 제거.
    lines_to_write.pop()
    # last-1 에는 개행문자 제거
    last_line = lines_to_write.pop()
    last_line = last_line.replace('\n', '')
    lines_to_write.append(last_line)

    for line in lines_to_write:
        output_file.write(f'{get_date},{line}')

output_file.close()

print(f'Output 파일 생성 완료 {output_file_name}')

# BigQuery 업로드 준비를 위해 gcs 에 업로드
project_id = 'sc-data-mart'
bucket_name = 'aaa-general-purpose'

storage_client = storage.Client(project=project_id)
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(output_file_name)
blob.upload_from_filename(f'files/{output_file_name}')

print(f'Output 파일 GCS 업로드 완료 {output_file_name}')

# Target bigquery table 에 정보 적재
bigquery_client = bigquery.Client(project=project_id)
dataset_name = 'en_biz_common_data'
table_name = 'generator_capacity_statistics'

table_id = f'{project_id}.{dataset_name}.{table_name}'

job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,    # 첫 번째 행은 columns
    max_bad_records=100,
    schema=[
        bigquery.SchemaField("date", "DATE"),
        bigquery.SchemaField("company", "STRING"),
        bigquery.SchemaField("generator", "STRING"),
        bigquery.SchemaField("hogi", "INT64"),
        bigquery.SchemaField("capacity", "FLOAT64"),
        bigquery.SchemaField("user_type", "STRING"),
        bigquery.SchemaField("pw_dispatch_type", "STRING"),
        bigquery.SchemaField("pw_source", "STRING"),
        bigquery.SchemaField("pw_gen_type", "STRING"),
        bigquery.SchemaField("biz_type", "STRING"),
        bigquery.SchemaField("gwangyeok", "STRING"),
        bigquery.SchemaField("sebu", "STRING")
    ]
)

gs_file_uri = f'gs://{bucket_name}/{output_file_name}'

load_job = bigquery_client.load_table_from_uri(
    gs_file_uri, table_id, job_config=job_config
)   # This makes an API request.

load_job.result()   # Waits for the job to complete.

# 업로드 결과 확인
destination_table = bigquery_client.get_table(table_id)

print(f'Row 갯수 : {destination_table.num_rows}')

# 다 마치면 로컬 및 gcs 에서 파일 삭제
if os.path.exists(f'files/{output_file_name}'):
    os.remove(f'files/{output_file_name}')
    print('임시 파일 삭제 완료 - ' + output_file_name)
else:
    print('임시 파일 없음')

blob.delete()
print(f'임시 파일 {output_file_name} 을 버킷에서 삭제.')