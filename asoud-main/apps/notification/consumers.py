from channels.generic.websocket import AsyncWebsocketConsumer
import json
from apps.notification.validator import validate_user
from channels.db import database_sync_to_async


# Define a function that calls is_owner
def check_is_owner(user):
    return user.is_owner()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("conncting to notification system")
        # Authenticate user
        user = await validate_user(self.scope)

        if user is None:
            await self.close()
            return
        
        self.scope["user"] = user

        if user.is_authenticated:
            await self.accept()
            await self.channel_layer.group_add(f"user_{user.id}", self.channel_name)

            check_owner = database_sync_to_async(check_is_owner)
            if await check_owner(user):
                await self.channel_layer.group_add("owners", self.channel_name)
                print(f"Owner {user.id} added to the 'owners' group.")

        else:
            await self.close()

    async def disconnect(self, close_code):
        # Remove the user from the group
        user = self.scope["user"]
        if user.is_authenticated:
            await self.channel_layer.group_discard(f"user_{user.id}", self.channel_name)

    async def send_notification(self, event):
        print('sending a notification to ', event['data'])
        await self.send(text_data=json.dumps(event["data"]))