import json
import os
import mlflow
import requests
from requests.auth import HTTPBasicAuth


# 확인 필요 1. Keycloak 으로 부터 Authorization header 에 넣을 수 있는 token 을 발급 받을 수 있는가?

client_id = "mlflow"
client_secret = "WbIR7iHUYhSj4mA4yEoSjEAFPTHmktpk"
token_url = "https://keycloak-1.enlighten.kr/realms/EN_Dev/protocol/openid-connect/token"
payload = 'grant_type=client_credentials'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request(method='POST',
                            url=token_url,
                            headers=headers,
                            data=payload,
                            auth=HTTPBasicAuth(client_id, client_secret))

access_token = json.loads(response.text)['access_token']
print(access_token)
# 확인 필요 2. 위에서 받은 access_token 으로 실제 자원 접근 가능한지 확인

mlflow_url = 'https://mlflow.dev.enlighten.kr?origin=app'
experiment_name = 'Default'

## HTTP 인증 주입 방법 : https://mlflow.org/docs/latest/tracking.html
os.environ['MLFLOW_TRACKING_TOKEN'] = access_token

mlflow.set_tracking_uri(mlflow_url)
print(mlflow.is_tracking_uri_set())
print(mlflow.get_tracking_uri())
experiment = mlflow.get_experiment_by_name(experiment_name)
print(experiment)