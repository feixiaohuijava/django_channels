# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
from mysite.settings import BASE_DIR
import time

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        while True:
            time.sleep(3)
            file = open(BASE_DIR + '/chat/' + 'deploy.log')
            for line in file:
                self.send(text_data=json.dumps({'message':line}))


        # time.sleep(3)
        # print(text_data)
        # self.send(text_data=json.dumps({'message':'nihao'}))
        # time.sleep(3)
        # self.send(text_data=json.dumps({'message':'python'}))
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