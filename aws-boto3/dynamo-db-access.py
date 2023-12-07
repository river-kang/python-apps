import boto3
from boto3.dynamodb.conditions import Key, Attr

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Specify your table name
table_name = 'ems_site_data'
table = dynamodb.Table(table_name)

# Specify the site_id you want to query
site_id_value = 1

# Query the table
response = table.query(
    KeyConditionExpression=Key('site_id').eq(site_id_value),
    ScanIndexForward=False,  # This sorts the results in descending order
    Limit=1  # This limits the result to only the most recent item
)

# Extract the most recent record
latest_record = response['Items'][0] if response['Items'] else None

# Print the latest record
print(latest_record)