import json
from google.cloud import pubsub_v1


def callback(message: pubsub_v1.subscriber.message.Message):
    # https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.subscriber.message.Message
    # The type of message.data is byte string. Need to be converted to UTF-8 string
    print(message)
    json_decoded_data = json.loads(message.data.decode('UTF-8'))

    print(json_decoded_data)

    message.ack()

dummy_topic_default_sub_name = "dummy-topic-default-sub"
rtu_v1_binary_sub_name = "rtu-v1-inverter-raw-data-bq-loader-rtu_binary_stream"


if __name__ == "__main__":
    with pubsub_v1.SubscriberClient() as subscriber:
        subscription_path = subscriber.subscription_path("en-data-mart-dev-id-0128",
                                                         rtu_v1_binary_sub_name)
        print(f"Listening for messages on {subscription_path}..")
        future = subscriber.subscribe(subscription_path, callback)

        try:
            future.result(None)
        except TimeoutError:
            print(f"Timeout 이외 에러 발생. 동작 중단.")
            future.cancel()
