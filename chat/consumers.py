# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
from mysite.settings import BASE_DIR
import time
import linecache

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        print("websocket disconnect")

    def receive(self, text_data):
        start_count = 0
        while True:
            filepath = BASE_DIR + '/chat/' + 'deploy.log'
            end_count = len(open(filepath, 'rU').readlines())
            if end_count > start_count:
                file = open(filepath, 'rU')
                temp_count = 1
                for line in file:
                    if temp_count > start_count and temp_count <=end_count:
                        self.send(text_data=json.dumps({'message':line}))
                    else:
                        pass
                    temp_count += 1
                start_count = end_count
