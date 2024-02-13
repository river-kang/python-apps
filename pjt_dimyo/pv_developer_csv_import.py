from google.cloud import bigquery

# Initialize a BigQuery client
client = bigquery.Client()

# Define your table ID and job configuration
table_id = "sc-data-mart.en_biz_common_data.pv_developers"
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    schema=[
        bigquery.SchemaField(name="year", field_type="INTEGER", mode="REQUIRED"),
        bigquery.SchemaField(name="name", field_type="STRING", mode="REQUIRED"),
        bigquery.SchemaField(name="gwangyeok", field_type="STRING", mode="REQUIRED"),
        bigquery.SchemaField(name="biz_reg_num", field_type="STRING", mode="REQUIRED"),
        bigquery.SchemaField(name="president", field_type="STRING", mode="REQUIRED"),
        bigquery.SchemaField(name="address", field_type="STRING", mode="REQUIRED"),
        bigquery.SchemaField(name="loc_coord", field_type="GEOGRAPHY", mode="REQUIRED"),
        bigquery.SchemaField(name="note", field_type="STRING", mode="REQUIRED"),
        bigquery.SchemaField(name="total_capa", field_type="FLOAT", mode="NULLABLE"),
        bigquery.SchemaField(name="total_prj_num", field_type="INTEGER", mode="NULLABLE"),
        bigquery.SchemaField(name="relation", field_type="STRING", mode="NULLABLE"),
    ],
    autodetect=False,
)

# Specify the path to your JSON file
file_path = "files/2023_pv_developer_sample.json"

with open(file_path, "rb") as source_file:
    load_job = client.load_table_from_file(
        source_file, table_id, job_config=job_config
    )

# Wait for the load job to complete
load_job.result()

print("Load job finished.")