import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        
        #Catch the name of the room
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        #Join the room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        #Accept the connection
        await self.accept()


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    
    async def receive(self, text_data):
        
        #Receive information from the client and we spread it
        text_data_json = json.loads(text_data)
        name = text_data_json["name"]
        text = text_data_json["text"]
        print('sending...')
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type': "chat_message",
                'name': name,
                'text': text
            }
        )


    async def chat_message(self, event):

        name = event.get('name')
        text = event.get('text')
        print(text)
        await self.send(
            text_data=json.dumps(
                {
                    'type': 'chat_message',
                    'name': name,
                    'text': text
                }
            )
        )