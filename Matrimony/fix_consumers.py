import re

file_path = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony-2807-2\Matrimony\Matrimony\interactions_app\consumers.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add video call routing to receive method
receive_patch = """
        elif action in ['video_call_invite', 'video_call_accept', 'video_call_reject']:
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
"""

content = content.replace("        message = data.get('message')", receive_patch)

# Add video_call_signal method
signal_patch = """
    async def video_call_signal(self, event):
        await self.send(text_data=json.dumps({
            'action': event.get('action'),
            'room_id': event.get('room_id'),
            'sender_id': event.get('sender_id')
        }))

    @database_sync_to_async
"""

content = content.replace("    @database_sync_to_async\n    def check_message_limit", signal_patch + "    def check_message_limit")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated consumers.py successfully.")
