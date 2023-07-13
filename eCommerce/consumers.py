
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Clean up any resources on WebSocket disconnect
        pass

    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        # Here you can process any custom logic for notifications

        # Example: Echo the received message back to the client
        await self.send(text_data=json.dumps({
            'message': text_data
        }))
