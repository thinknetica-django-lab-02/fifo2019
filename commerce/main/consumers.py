# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from main.models import Product
import uuid


class ChatBot(WebsocketConsumer):
    def connect(self):
        unic = uuid.uuid4().hex
        self.group_name = f"chat_{unic}"

        self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):

        self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        in_stock = ''
        product_name = ''
        product = Product.objects.filter(title=message).first()
        if product is not None:
            in_stock = product.quantity
            product_name = product.title

        self.send(text_data=json.dumps({
            'in_stock': in_stock,
            'product_name': product_name,
        }))
