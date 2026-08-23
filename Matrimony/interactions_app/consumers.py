import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatMessage
from profiles_app.models import Profile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Get user from scope
        self.user = self.scope.get('user')
        if self.user and self.user.is_authenticated:
            await self.set_online_status(self.user.id, True)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        # Broadcast presence
        if self.user and self.user.is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'presence_update',
                    'user_id': self.user.id,
                    'is_online': True
                }
            )

    async def disconnect(self, close_code):
        if hasattr(self, 'user') and self.user and self.user.is_authenticated:
            await self.set_online_status(self.user.id, False)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'presence_update',
                    'user_id': self.user.id,
                    'is_online': False
                }
            )

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action', 'chat_message')
        
        if action == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'sender_id': data.get('sender_id'),
                    'is_typing': data.get('is_typing', True)
                }
            )
            return
            
        elif action == 'read_receipt':
            sender_id = data.get('sender_id') # person who read
            await self.mark_messages_read(data.get('receiver_id'), sender_id)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'read_receipt',
                    'reader_id': sender_id
                }
            )
            return


        elif action in ['video_call_invite', 'video_call_accept', 'video_call_reject', 'audio_call_invite', 'audio_call_accept', 'audio_call_reject']:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'video_call_signal',
                    'action': action,
                    'room_id': data.get('room_id'),
                    'sender_id': data.get('sender_id')
                }
            )
            return

        message = data.get('message')

        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')

        # Check daily message limit
        can_send = await self.check_message_limit(sender_id)
        if not can_send:
            await self.send(text_data=json.dumps({
                'action': 'limit_reached',
                'message': 'You have reached your daily message limit for your current plan.'
            }))
            return

        # Save to database
        chat_msg = await self.save_message(sender_id, receiver_id, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'action': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'message_id': chat_msg.id
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'action': 'chat_message',
            'message': event.get('message'),
            'sender_id': event.get('sender_id'),
            'message_id': event.get('message_id'),
            'delete_msg_id': event.get('delete_msg_id')
        }))
        
    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'action': 'typing',
            'sender_id': event.get('sender_id'),
            'is_typing': event.get('is_typing')
        }))
        
    async def read_receipt(self, event):
        await self.send(text_data=json.dumps({
            'action': 'read_receipt',
            'reader_id': event.get('reader_id')
        }))
        
    async def presence_update(self, event):
        await self.send(text_data=json.dumps({
            'action': 'presence',
            'user_id': event.get('user_id'),
            'is_online': event.get('is_online')
        }))


    async def video_call_signal(self, event):
        await self.send(text_data=json.dumps({
            'action': event.get('action'),
            'room_id': event.get('room_id'),
            'sender_id': event.get('sender_id')
        }))

    @database_sync_to_async
    def check_message_limit(self, sender_id):
        from django.utils import timezone
        sender = User.objects.get(id=sender_id)
        
        # Admin or Unpaid (should not happen, but safe fallback)
        if sender.is_superuser or sender.is_staff: return True
        if not hasattr(sender, 'profile'): return True
        profile = sender.profile
        if profile.payment_status != 'Paid' or not profile.active_plan:
            return False
            
        plan_name = profile.active_plan.name.lower()
        
        limit = -1
        if 'bronze' in plan_name:
            limit = 20
        elif 'silver' in plan_name:
            limit = 100
        elif 'gold' in plan_name:
            limit = -1
            
        if limit == -1: return True
        
        today = timezone.now().date()
        sent_today = ChatMessage.objects.filter(sender=sender, timestamp__date=today).count()
        return sent_today < limit

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        return ChatMessage.objects.create(sender=sender, receiver=receiver, message=content)
        
    @database_sync_to_async
    def set_online_status(self, user_id, is_online):
        try:
            from django.utils import timezone
            Profile.objects.filter(user_id=user_id).update(last_activity=timezone.now() if is_online else None)
        except Exception:
            pass
            
    @database_sync_to_async
    def mark_messages_read(self, sender_id, receiver_id):
        # Mark all messages sent by sender_id to receiver_id as read
        ChatMessage.objects.filter(sender_id=sender_id, receiver_id=receiver_id, is_read=False).update(is_read=True)

