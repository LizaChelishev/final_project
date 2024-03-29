from DataBaseGenerator.RabbitConsumer import RabbitConsumerObject
from threadLockManager import ThreadLockManager

import json
import threading


lock_manager = ThreadLockManager.get_instance()


def main():
    rabbit = RabbitConsumerObject(q_name='db_responses', callback=callback)
    rabbit.consume()


def callback(ch, method, properties, body):
    data = json.loads(body)  # reading the data
    print(data)
    request_id = data['id_']  # getting the request id
    lock_manager.handle_answer_release_thread(request_id=request_id, data=data)


t = threading.Thread(target=main)
t.setDaemon(True)
t.start()