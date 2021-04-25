from django.urls import path

from main import consumers

websocket_urlpatterns = [
    path("ws/chatbot/", consumers.ChatBot.as_asgi()),
]
