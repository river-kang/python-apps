import json
from google.cloud import pubsub_v1


def callback_first(message: pubsub_v1.subscriber.message.Message):
    # https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.subscriber.message.Message
    # The type of message.data is byte string. Need to be converted to UTF-8 string
    print('First pubsub\'s callback')
    print(message)
    print(subscription_path1)


def callback_second(message: pubsub_v1.subscriber.message.Message):
    # https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.subscriber.message.Message
    # The type of message.data is byte string. Need to be converted to UTF-8 string
    print('Second pubsub\'s callback')
    print(message)


def callback_third(message: pubsub_v1.subscriber.message.Message):
    # https://cloud.google.com/python/docs/reference/pubsub/latest/google.cloud.pubsub_v1.subscriber.message.Message
    # The type of message.data is byte string. Need to be converted to UTF-8 string
    print('Third pubsub\'s callback')
    print(message)


if __name__ == "__main__":
    # 여기 아래는 모두 global scope 에 속하는 변수들이다.
    # 왜냐하면 위의 조건문 자체가 global 에서 동작하기 때문이다.
    # 그래서 다른 함수들에서 여기 안에 정의된 변수들은 참조가 된다.
    subscriber1 = pubsub_v1.SubscriberClient()
    subscription_path1 = subscriber1.subscription_path("en-data-mart-dev-id-0128",
                                                         "test-sub-1")
    print(f"Listening for messages on {subscription_path1}..\n")
    future1 = subscriber1.subscribe(subscription_path1, callback_first)

    subscriber2 = pubsub_v1.SubscriberClient()
    subscription_path2 = subscriber2.subscription_path("en-data-mart-dev-id-0128",
                                                         "test-sub-2")
    print(f"Listening for messages on {subscription_path2}..\n")
    future2 = subscriber2.subscribe(subscription_path2, callback_second)

    subscriber3 = pubsub_v1.SubscriberClient()
    subscription_path3 = subscriber3.subscription_path("en-data-mart-dev-id-0128",
                                                         "test-sub-3")
    print(f"Listening for messages on {subscription_path3}..\n")
    future3 = subscriber3.subscribe(subscription_path3, callback_third)

    with subscriber1, subscriber2, subscriber3:
        future1.result()
        future2.result()
        future3.result()

