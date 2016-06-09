#!/usr/bin/env python
import pika
import json
import requests

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.queue_declare(queue='slack')

def callback(ch, method, properties, body):
    payload = {}
    payload["text"] = body
    r = requests.post(SLACK_WEBHOOK_URL, data = json.dumps(payload))

channel.basic_consume(callback, queue='slack', no_ack=True)
channel.start_consuming()
