# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Group
from django.contrib.auth import get_user_model

User = get_user_model()



# class ChatConsumer(WebsocketConsumer):

    

#     def __init__(self, *args, **kwargs):
#         self.count = 0
#         return super().__init__(*args, **kwargs)


#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )
#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         self.commands[data["command"]](self, data)


#     def messages_to_json(self, messages):
#         result = [message.to_json() for message in messages]
#         return result

#     # message : content = {"command": "messages", "messages": self.messages_to_json(messages)}
#     def send_message(self, message):
#         self.send(text_data=json.dumps(message))
        
#     # data: info related with group
#     def fetch_old_messages(self, data): 
#         name = data["name"]
#         group = Group.objects.get(name=name)
#         messages = group.last_10_messages(times=self.count)
#         if messages:
#             self.count += 1
#         else:
#             self.count -= 1
#             messages = group.last_10_messages(times=self.count)

#         content = {"command": "messages", "messages": self.messages_to_json(messages)}
#         self.send_message(content)


#     def fetch_messages(self, data):
#         self.count = 0
#         name = data["name"]
#         group = Group.objects.get(name=name)
#         messages = group.last_10_messages(times=self.count)
#         content = {"command": "messages", "messages": self.messages_to_json(messages)}
#         self.send_message(content)


#     def groups_to_json(self, groups):
#         result = [group.to_json() for group in groups]
#         return results

#     def fetch_groups(self, data):
#         user_name = data["username"]
#         user = User.objects.get(username=user_name)
#         groups = user.all_groups.all()
#         content = {
#             "command" : "groups",
#             "groups" : self.groups_to_json(groups),
#         }
#         self.send_message(content)    

#     def new_message(self, data):
#         author_name = data["from"]
#         group_name = data["name"]
#         author = User.objects.get(username=author_name)
#         group = Group.objects.get(name=group_name)
#         message = Messages.objects.create(
#             group=group,
#             author=author,
#             text=data["message"],
#         )
#         content = {"command": "new_message", "message": message.to_json()}
#         return self.send_chat_message(content)

#     commands = {
#         "fetch_old_messages": fetch_old_messages,
#         "fetch_messages": fetch_messages,
#         "new_message": new_message,
#         "fetch_groups" : fetch_groups,
#     }
    

    
#     # meessage : content = {"command": "new_message", "message": message.to_json()}
#     def send_chat_message(self, message):
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )


#     def chat_message(self, event):
#         message = event["message"]
#         self.send(text_data=json.dumps(message))


    

    

    

    


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


