from confluent_kafka import Producer

producer = Producer()

producer.flush()