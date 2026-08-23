import re

file_path = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony-2807-2\Matrimony\Matrimony\Template\web\chat.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Video/Audio Call buttons with IDs
content = content.replace(
    '<button title="Video Call">',
    '<button title="Video Call" id="start-video-call">'
)

# 2. Add Jitsi script to head or before closing body
jitsi_and_modal = """
<!-- Jitsi Script -->
<script src='https://meet.jit.si/external_api.js'></script>

<!-- Video Call Modal overlay -->
<div class="modal fade" id="videoCallModal" tabindex="-1" aria-hidden="true" data-bs-backdrop="static">
  <div class="modal-dialog modal-xl modal-dialog-centered">
    <div class="modal-content" style="background: #1e293b; border: none; border-radius: 15px; overflow: hidden;">
      <div class="modal-header border-0" style="padding: 10px 20px;">
        <h5 class="modal-title text-white"><i class="fa-solid fa-video me-2 text-danger"></i> ForeverBond Call</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close" id="end-call-btn"></button>
      </div>
      <div class="modal-body p-0" id="jitsi-container" style="height: 70vh; width: 100%;">
      </div>
    </div>
  </div>
</div>

<!-- Incoming Call Alert Modal -->
<div class="modal fade" id="incomingCallModal" tabindex="-1" aria-hidden="true" data-bs-backdrop="static">
  <div class="modal-dialog modal-dialog-centered modal-sm">
    <div class="modal-content text-center" style="border-radius: 20px; border: none; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
      <div class="modal-body p-4">
        <div class="mb-3">
          <div class="spinner-grow text-danger" role="status" style="width: 3rem; height: 3rem;">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <h5 class="fw-bold mb-1">Incoming Video Call</h5>
        <p class="text-muted mb-4">You have a call from <span id="incoming-caller-name" class="fw-bold text-dark">User</span></p>
        
        <div class="d-flex justify-content-center gap-3">
          <button class="btn btn-danger rounded-circle p-3 shadow-sm" id="reject-call-btn" style="width: 60px; height: 60px;">
            <i class="fa-solid fa-phone-slash fs-4"></i>
          </button>
          <button class="btn btn-success rounded-circle p-3 shadow-sm" id="accept-call-btn" style="width: 60px; height: 60px;">
            <i class="fa-solid fa-phone fs-4"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
"""

content = content.replace("</body>", jitsi_and_modal + "\n</body>")

# 3. Add Video Call Javascript inside the DOMContentLoaded block
js_patch = """
          // -------------- JITSI VIDEO CALL LOGIC --------------
          let api = null;
          let currentRoomId = null;
          
          const startVideoCallBtn = document.getElementById('start-video-call');
          const videoCallModal = new bootstrap.Modal(document.getElementById('videoCallModal'));
          const incomingCallModal = new bootstrap.Modal(document.getElementById('incomingCallModal'));
          const jitsiContainer = document.getElementById('jitsi-container');
          
          function initJitsi(roomName) {
              jitsiContainer.innerHTML = '';
              const domain = 'meet.jit.si';
              const options = {
                  roomName: roomName,
                  width: '100%',
                  height: '100%',
                  parentNode: jitsiContainer,
                  userInfo: {
                      displayName: currentUserId // Could use actual name if available
                  },
                  configOverwrite: { startWithAudioMuted: false, startWithVideoMuted: false },
                  interfaceConfigOverwrite: { SHOW_JITSI_WATERMARK: false }
              };
              api = new JitsiMeetExternalAPI(domain, options);
              
              api.addEventListener('videoConferenceLeft', () => {
                  videoCallModal.hide();
                  if(api) {
                      api.dispose();
                      api = null;
                  }
              });
          }
          
          if(startVideoCallBtn) {
              startVideoCallBtn.addEventListener('click', () => {
                  // Generate room ID based on user IDs
                  const minId = Math.min(currentUserId, activeUserId);
                  const maxId = Math.max(currentUserId, activeUserId);
                  currentRoomId = `ForeverBond_Call_${minId}_${maxId}_${Date.now()}`;
                  
                  // Notify the other user
                  chatSocket.send(JSON.stringify({
                      'action': 'video_call_invite',
                      'room_id': currentRoomId,
                      'sender_id': currentUserId,
                      'receiver_id': activeUserId
                  }));
                  
                  // Join immediately
                  videoCallModal.show();
                  initJitsi(currentRoomId);
              });
          }
          
          document.getElementById('end-call-btn').addEventListener('click', () => {
              if(api) {
                  api.dispose();
                  api = null;
              }
          });
          
          document.getElementById('accept-call-btn').addEventListener('click', () => {
              incomingCallModal.hide();
              
              // Tell sender we accepted
              chatSocket.send(JSON.stringify({
                  'action': 'video_call_accept',
                  'room_id': currentRoomId,
                  'sender_id': currentUserId,
                  'receiver_id': activeUserId
              }));
              
              videoCallModal.show();
              initJitsi(currentRoomId);
          });
          
          document.getElementById('reject-call-btn').addEventListener('click', () => {
              incomingCallModal.hide();
              chatSocket.send(JSON.stringify({
                  'action': 'video_call_reject',
                  'room_id': currentRoomId,
                  'sender_id': currentUserId,
                  'receiver_id': activeUserId
              }));
          });
          // ----------------------------------------------------
"""

socket_handling_patch = """
          if (action === 'video_call_invite') {
              if (parseInt(data.sender_id) === parseInt(activeUserId)) {
                  currentRoomId = data.room_id;
                  document.getElementById('incoming-caller-name').innerText = document.querySelector('.chat-header-info h4').innerText;
                  incomingCallModal.show();
              }
              return;
          }
          if (action === 'video_call_reject') {
              if (parseInt(data.sender_id) === parseInt(activeUserId)) {
                  videoCallModal.hide();
                  if(api) { api.dispose(); api = null; }
                  alert("User rejected the call.");
              }
              return;
          }
"""

# Insert JS logic
content = content.replace('chatInput.addEventListener("keypress"', js_patch + '\n          chatInput.addEventListener("keypress"')
content = content.replace("if (action === 'typing')", socket_handling_patch + "          if (action === 'typing')")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated chat.html successfully.")
