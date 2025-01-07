import time
from confluent_kafka.admin import AdminClient, KafkaException
import confluent_kafka as ck
from typing import Callable


class Producer:
    def __init__(self, bootstrap_servers, client_id, acks: str = None, retries: int = None):
        self.__conf = {
            "bootstrap.servers": bootstrap_servers,
            "client.id": client_id,
            "acks": acks,
            "retries": retries
        }
        self.__producer = ck.Producer(**self.__conf)

    def produce(self, topic, value):
        self.__producer.produce(topic, value.encode('utf-8'))
        self.__producer.flush()


class Consumer:
    def __init__(self, bootstrap_servers, group_id, auto_offset_reset='earliest'):
        self.__conf = {
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": auto_offset_reset
        }
        self.__consumer = ck.Consumer(**self.__conf)

    def subscribe(self, topics):
        self.__consumer.subscribe(topics)

    def consume(self):
        return self.__consumer.poll(1.0)

    def close(self):
        self.__consumer.close()

    def __del__(self):
        self.close()


def consume_messages(consumer: Consumer, msg_callback: Callable[[str], None], success_callback: Callable[[str], None] = None, error_callback: Callable[[str], None] = None):
    def safe_callback(callback, value):
        if callback is not None:
            callback(value)

    try:
        while True:
            msg = consumer.consume()
            if msg is None:
                continue
            if msg.error() and msg.error().code != ck.KafkaError._PARTITION_EOF:
                safe_callback(error_callback,
                              f"Error while consuming message: {msg.error()}")
                continue
            safe_callback(msg_callback, msg.value().decode("utf-8"))
            safe_callback(success_callback, f"Received message: {msg.value()}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


# def topic_exists(admin_client, topic_name):
#     try:
#         metadata = admin_client.list_topics(timeout=10)
#         return topic_name in metadata.topics
#     except KafkaException as e:
#         print(f"Error listing topics: {e}")
#         return False
#
#
# def wait_for_topic(bootstrap, topic_name, timeout=60, interval=5):
#     admin_client = AdminClient({'bootstrap.servers': bootstrap})
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         if topic_exists(admin_client, topic_name):
#             print(f"Topic {topic_name} is ready.")
#             return
#         print(
#             f"Topic {topic_name} not yet available. Retrying in {interval} seconds...")
#         time.sleep(interval)
#         raise TimeoutError(
#             f"Timed out waiting for topic {topic_name} to be ready.")
