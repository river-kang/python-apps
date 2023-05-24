# Retrieve the list of existing buckets
import json

import boto3

iot = boto3.client('iot')
response = iot.get_v2_logging_options()

print(json.dumps(response, indent=4))