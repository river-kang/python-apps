import json
from google.cloud import pubsub_v1
from multiprocessing import Process, current_process


def callback_first(message: pubsub_v1.subscriber.message.Message):
    # https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.subscriber.message.Message
    # The type of message.data is byte string. Need to be converted to UTF-8 string
    print(f'First pubsub\'s callback in process {current_process().name}')
    print(message.data)
    message.ack()


def callback_second(message: pubsub_v1.subscriber.message.Message):
    # https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.subscriber.message.Message
    # The type of message.data is byte string. Need to be converted to UTF-8 string
    print(f'Second pubsub\'s callback in process {current_process().name}')
    print(message.data)
    message.ack()


def callback_third(message: pubsub_v1.subscriber.message.Message):
    # https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.subscriber.message.Message
    # The type of message.data is byte string. Need to be converted to UTF-8 string
    print(f'Third pubsub\'s callback in process {current_process().name}')
    print(message.data)
    message.ack()


def pubsub_subscribe_task(project_id, subscription_id, callback):
    with pubsub_v1.SubscriberClient() as subscriber:
        subscription_path = subscriber.subscription_path(project_id,
                                                         subscription_id)
        print(f"Listening for messages on {subscription_path}..\n")
        future = subscriber.subscribe(subscription_path, callback)

        try:
            future.result(None)
        except TimeoutError:
            print(f"Timeout 이외 에러 발생. 동작 중단.")
            future.cancel()


if __name__ == "__main__":
    # creating threads
    Process(target=pubsub_subscribe_task,
            args=["en-data-mart-dev-id-0128", "test-sub-1", callback_first]).start()
    Process(target=pubsub_subscribe_task,
            args=["en-data-mart-dev-id-0128", "test-sub-2", callback_second]).start()
    Process(target=pubsub_subscribe_task,
            args=["en-data-mart-dev-id-0128", "test-sub-3", callback_third]).start()
