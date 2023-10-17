import threading

from awsiot import mqtt_connection_builder
from awscrt import mqtt
import sys


def build_direct_mqtt_connection(endpoint,
                                 port,
                                 cert_filepath,
                                 pri_key_filepath,
                                 on_connection_interrupted_callback,
                                 on_connection_resumed_callback,
                                 client_id):
    return mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        port=port,
        cert_filepath=cert_filepath,
        pri_key_filepath=pri_key_filepath,
        on_connection_interrupted=on_connection_interrupted_callback,
        on_connection_resumed=on_connection_resumed_callback,
        client_id=client_id,
        clean_session=False,
        keep_alive_secs=30,
        http_proxy_options=None)


def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("Resubscribe results: {}".format(resubscribe_results))

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit("Server rejected resubscribe to topic: {}".format(topic))


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))


def subscribe_aws_iot_core_topic():
    mqtt_connection = build_direct_mqtt_connection(
        #endpoint="apivnvk74gjx5-ats.iot.ap-northeast-2.amazonaws.com",
        endpoint="a2aq9awfqr508r-ats.iot.ap-northeast-2.amazonaws.com",
        port=8883,
        cert_filepath='cert_prod.pem',
        pri_key_filepath='priv_prod.key',
        # ca_filepath='AmazonRootCAChain.pem',
        on_connection_interrupted_callback=on_connection_interrupted,
        on_connection_resumed_callback=on_connection_resumed,
        client_id='my-test-client'
    )

    print(f'Connecting to endpoint with client ID : my-test-client')
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    # Subscribe to a topic
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic='/mymqtt/exam',
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)

    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result['qos'])))


if __name__ == '__main__':
    subscribe_aws_iot_core_topic()

    wait_event = threading.Event()
    wait_event.wait()
