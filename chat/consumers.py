# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
import time

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        time.sleep(3)
        print(text_data)
        self.send(text_data=json.dumps({'message':'nihao'}))
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        #
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))
        # print("receive function")
        # time.sleep(3)
        # self.send(text_data=json.dumps({
        #     'message': 'nihao'
        # }))