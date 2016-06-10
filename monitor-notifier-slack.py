#!/usr/bin/env python
import pika
import json
import requests
import os

RABBIT_MQ_SERVER = os.environ["RABBIT_MQ_SERVER"]
RABBIT_MQ_USER = os.environ["RABBIT_MQ_USER"]
RABBIT_MQ_PWD = os.environ["RABBIT_MQ_PWD"]

credentials = pika.PlainCredentials(RABBIT_MQ_USER, RABBIT_MQ_PWD)

connection = pika.BlockingConnection(pika.ConnectionParameters(
               RABBIT_MQ_SERVER, credentials = credentials))
channel = connection.channel()

def callback(ch, method, properties, body):
    payload = {}
    req = json.loads(body)
    check_type = req["monitor"]["result"]["check"]["type"]
    host = json.loads(req["monitor"]["result"]["check"]["arguments"])["host"]
    time = req["monitor"]["result"]["timestamp"]
    payload["text"] = check_type + " check failed for " + host + " at " + time
    webhook_url = json.loads(req["monitor"]["notifier"]["arguments"])["webhook_url"]
    r = requests.post(webhook_url, data = json.dumps(payload))

channel.basic_consume(callback, queue='slack', no_ack=True)
channel.start_consuming()
