import json
from google.cloud import pubsub_v1

dev_ids = set()


def general_callback(message: pubsub_v1.subscriber.message.Message):
    # https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.subscriber.message.Message
    # The type of message.data is byte string. Need to be converted to UTF-8 string
    print(message)
    json_decoded_data = json.loads(message.data.decode('UTF-8'))

    print(json_decoded_data)
    message.ack()

def rtu_v1_connection_status_callback(message: pubsub_v1.subscriber.message.Message):
    # https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.subscriber.message.Message
    # The type of message.data is byte string. Need to be converted to UTF-8 string
    print(message)
    json_decoded_data = json.loads(message.data.decode('UTF-8'))

    print(json_decoded_data)
    message.ack()


def residual_check_subscription_callback(message: pubsub_v1.subscriber.message.Message):
    # https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.subscriber.message.Message
    # The type of message.data is byte string. Need to be converted to UTF-8 string
    # print(message)
    json_decoded_data = json.loads(message.data.decode('UTF-8'))

    # print(json_decoded_data)

    dev_ids.add(message.attributes["deviceId"])

    print(dev_ids)
    message.ack()

project_id = "en-data-mart-dev-id-0128"

# subscription_name = "residual-check-subscription"
# subscription_name = "rtu-v1-connection-status-sub-default"
subscription_name = "eims-usage-sub"

if __name__ == "__main__":
    with pubsub_v1.SubscriberClient() as subscriber:
        subscription_path = subscriber.subscription_path(project_id,
                                                         subscription_name)
        print(f"Listening for messages on {subscription_path}..")
        future = subscriber.subscribe(subscription_path, general_callback)

        try:
            future.result(None)
        except TimeoutError:
            print(f"Timeout 이외 에러 발생. 동작 중단.")
            future.cancel()
