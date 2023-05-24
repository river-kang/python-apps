import mlflow

mlflow_url = 'https://mlflow.enlighten.kr'
experiment_name = 'Default'

## HTTP 인증 주입 방법 : https://mlflow.org/docs/latest/tracking.html
mlflow.set_tracking_uri(mlflow_url)
print(mlflow.is_tracking_uri_set())
print(mlflow.get_tracking_uri())
experiment = mlflow.get_experiment_by_name(experiment_name)
print(experiment)