import os
import re

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\chat.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

ws_script = '''    <!-- Chat Dynamic Data Script -->
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        const urlParams = new URLSearchParams(window.location.search);
        const activeUserId = urlParams.get("id");
        const name = urlParams.get("name");
        const img = urlParams.get("img");

        const chatMessages = document.querySelector(".chat-messages");
        const chatInput = document.querySelector(".chat-input-wrapper input");
        const sendBtn = document.querySelector(".send-btn");
        const chatContainer = document.querySelector(".chat-main");

        if (!activeUserId) {
            chatContainer.innerHTML = '<div style="display:flex; height:100%; width:100%; align-items:center; justify-content:center; flex-direction:column; color:#94a3b8;"><i class="fa-solid fa-comments" style="font-size:4rem; margin-bottom:15px; color:#e2e8f0;"></i><h4>Your Messages</h4><p>Select a connection from the sidebar to start chatting.</p></div>';
            return;
        }

        if (name) {
          const headerName = document.querySelector(".chat-user-details h5");
          if (headerName) headerName.innerHTML = name + ' <i class="fa-solid fa-circle-check" style="color: #10b981; font-size: 12px;" title="Verified"></i>';
        }
        if (img) {
          document.querySelectorAll(".contact-avatar").forEach((el) => {
              if(el.closest('.chat-header')) el.src = img;
          });
        }
        
        const isOnline = urlParams.get("online") === 'true';
        const statusDiv = document.querySelector(".chat-user-status");
        if (statusDiv) {
            if (isOnline) {
                statusDiv.innerHTML = '<i class="fa-solid fa-circle" style="color:#10b981;"></i> Online';
                statusDiv.style.color = '#10b981';
            } else {
                statusDiv.innerHTML = '<i class="fa-solid fa-circle" style="color:#ccc;"></i> Offline';
                statusDiv.style.color = '#64748b';
            }
        }

        const scrollToBottom = () => {
          chatMessages.scrollTop = chatMessages.scrollHeight;
        };

        const escapeHTML = (str) => {
          return str.replace(/[&<>'"]/g, (tag) => ({"&": "&amp;","<": "&lt;",">": "&gt;","'": "&#39;",'"': "&quot;"})[tag] || tag);
        };
        
        const formatTime = (isoString) => {
            const date = new Date(isoString);
            return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        };

        const loadMessages = () => {
            fetch(`/interactions/api/fetch-messages/${activeUserId}/`)
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success') {
                        chatMessages.innerHTML = '';
                        if(data.messages.length === 0) {
                            chatMessages.innerHTML = '<div style="text-align:center; margin-top:20px; color:#94a3b8; font-size:13px;" id="noMsg">Say hi to start the conversation!</div>';
                            return;
                        }
                        
                        data.messages.forEach(msg => {
                            const isOutgoing = msg.is_outgoing;
                            const bubble = document.createElement("div");
                            bubble.className = isOutgoing ? "message outgoing" : "message incoming";
                            bubble.innerHTML = `
                              <div class="message-bubble">${escapeHTML(msg.message)}</div>
                              <span class="message-time">${formatTime(msg.timestamp)} ${isOutgoing ? '<i class="fa-solid fa-check" style="color: #10b981"></i>' : ''}</span>
                            `;
                            chatMessages.appendChild(bubble);
                        });
                        scrollToBottom();
                    }
                })
                .catch(err => console.error("Error loading messages:", err));
        };

        loadMessages();

        // WebSocket Integration
        const currentUserId = "{{ request.user.id }}";
        // Create unique room name based on user IDs
        const roomName = [parseInt(currentUserId), parseInt(activeUserId)].sort((a,b)=>a-b).join('_');
        const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
        const chatSocket = new WebSocket(wsScheme + '://' + window.location.host + '/ws/chat/' + roomName + '/');

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            const isOutgoing = (parseInt(data.sender_id) === parseInt(currentUserId));
            
            const noMsg = document.getElementById("noMsg");
            if (noMsg) noMsg.remove();
            
            const bubble = document.createElement("div");
            bubble.className = isOutgoing ? "message outgoing" : "message incoming";
            bubble.innerHTML = `
              <div class="message-bubble">${escapeHTML(data.message)}</div>
              <span class="message-time">${formatTime(new Date())} ${isOutgoing ? '<i class="fa-solid fa-check" style="color: #10b981"></i>' : ''}</span>
            `;
            chatMessages.appendChild(bubble);
            scrollToBottom();
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        window.deleteChat = (type) => {
            if (!activeUserId) return;
            const msg = type === 'for_me' ? "Are you sure you want to delete this chat for yourself?" : "Are you sure you want to permanently delete this chat for everyone?";
            if (confirm(msg)) {
                fetch(`/interactions/api/delete-chat/${activeUserId}/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ delete_type: type })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success') {
                        chatMessages.innerHTML = '<div style="text-align:center; margin-top:20px; color:#94a3b8; font-size:13px;">Chat deleted successfully.</div>';
                        alert("Chat deleted successfully.");
                    } else {
                        alert(data.message);
                    }
                });
            }
        };

        const sendMessage = () => {
          const text = chatInput.value.trim();
          if (!text) return;
          chatInput.value = "";
          
          // Send via WebSocket instead of fetch
          chatSocket.send(JSON.stringify({
              'message': text,
              'sender_id': currentUserId,
              'receiver_id': activeUserId
          }));
        };

        sendBtn.addEventListener("click", sendMessage);
        chatInput.addEventListener("keypress", (e) => {
          if (e.key === "Enter") sendMessage();
        });
      });
    </script>'''

# Replace old script with new script
start_str = '<!-- Chat Dynamic Data Script -->'
end_str = '</script>'
# Find the position of start_str
start_idx = content.find(start_str)
if start_idx != -1:
    end_idx = content.find(end_str, start_idx) + len(end_str)
    content = content[:start_idx] + ws_script + content[end_idx:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated chat.html to use WebSockets')
else:
    print('Could not find start str')
