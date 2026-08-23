/* ==========================================================================
   MATRIMONY PORTAL GLOBAL CARD ACTIONS & REDIRECTIONS (card_actions.js)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  // --- 1. EXPRESS INTEREST HANDLER ---
  const handleInterestClick = async (button, sentText) => {
    // Find name
    const card = button.closest('.glass-card') || button.closest('.pm-profile-card') || button.closest('.profile-card-col');
    const nameEl = card ? (card.querySelector('h3')) : null;
    let name = nameEl ? nameEl.innerText.trim() : "Match";
    name = name.replace(/o"|Verified/g, '').trim();

    let userId = button.getAttribute('data-user-id');
    if (!userId && card) {
      const expressBtn = card.querySelector('[data-user-id]');
      if (expressBtn) userId = expressBtn.getAttribute('data-user-id');
    }

    if (button.dataset.status === 'sent') {
      // Mocking the backend ACCEPT manually for UI testing
      try {
        const payload = userId ? {receiver_id: userId} : {receiver_name: name};
        const response = await fetch('/interactions/api/accept-interest/', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(payload)
        });
        const data = await response.json();
        
        if (data.status === 'accepted') {
          button.dataset.status = 'accepted';
          button.innerHTML = '<i class="fa-solid fa-heart"></i> Accepted';
          button.style.background = 'linear-gradient(135deg, #10b981, #059669)';
          button.style.color = 'white';
          button.style.opacity = '1';
          button.style.cursor = 'default';
          showCustomToast('Interest accepted by backend! You can now chat.');
        } else {
          showCustomToast('Error: ' + data.message);
        }
      } catch (err) {
        console.error(err);
      }
      return;
    }
    
    if (button.dataset.status === 'accepted') return;

    try {
        const payload = userId ? {receiver_id: userId} : {receiver_name: name};
        const response = await fetch('/interactions/api/express-interest/', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(payload)
        });
        const data = await response.json();
        if (data.status === 'pending') {
            button.dataset.status = 'sent';
            button.innerHTML = sentText;
            showCustomToast(`Interest request successfully sent to ` + name + ` via Backend!`);
        } else if (data.status === 'error') {
            showCustomToast('Error: ' + data.message);
        }
    } catch (err) {
        console.error(err);
    }
  };

  // Bind to Premium Glass Cards
  document.querySelectorAll(".btn-premium-gradient").forEach(button => {
    if (button.innerText.trim().toLowerCase().includes("interest")) {
      button.addEventListener("click", (e) => {
        e.preventDefault();
        handleInterestClick(button, '<i class="fa-solid fa-check"></i> Interest Sent');
      });
    }
  });

  // Bind to PM Profile Cards
  document.querySelectorAll(".pm-interest-btn").forEach(button => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      handleInterestClick(button, '<i class="fa-solid fa-check"></i> Interest Sent');
    });
  });

  // --- 2. MESSAGE & CHAT REDIRECTION ---
  const redirectToChat = async (card) => {
    if (!card) return;
    
    // Extract name
    const nameEl = card.querySelector('h3');
    let name = nameEl ? nameEl.innerText.trim() : "ForeverBond Member";
    name = name.replace(/o"|Verified/g, '').trim();
    
    let userId = null;
    const expressBtn = card.querySelector('[data-user-id]');
    if (expressBtn) userId = expressBtn.getAttribute('data-user-id');

    try {
        // Query backend for actual interest status
        const payload = userId ? {receiver_id: userId} : {receiver_name: name};
        const response = await fetch('/interactions/api/check-interest/', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(payload)
        });
        const data = await response.json();
        
        if (data.status !== 'accepted') {
            if (data.status === 'pending') {
                showCustomToast("Chat will be unlocked once they accept your interest (Backend Checked).");
            } else {
                showCustomToast("Please express your interest first before chatting (Backend Checked).");
            }
            return;
        }
        
        // Extract image
        const imgEl = card.querySelector('img');
        const img = imgEl ? imgEl.src : '';

        // Redirect to chat page with dynamic parameters
        if (userId) {
            window.location.href = `/interactions/chat/?id=` + userId;
        } else {
            window.location.href = `/interactions/chat/?name=` + encodeURIComponent(name) + `&img=` + encodeURIComponent(img);
        }
        
    } catch (err) {
        console.error(err);
        showCustomToast("Could not verify interest status from backend.");
    }
  };

  // Bind to Message stack buttons on Glass Cards
  document.querySelectorAll(".btn-msg-stacked").forEach(btn => {
    btn.style.cursor = "pointer";
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const card = btn.closest('.glass-card');
      redirectToChat(card);
    });
  });

  // Bind to "View Biodata" or equivalent buttons on PM Profile Cards
  document.querySelectorAll(".pm-biodata-btn").forEach(btn => {
    btn.innerText = "? Message Chat"; // Make it explicitly clear it opens Chat
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const card = btn.closest('.pm-profile-card');
      redirectToChat(card);
    });
  });

  // Bind to Chat actions on Verified Profile Cards
  document.querySelectorAll(".open-chat-action").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const card = btn.closest('.profile-card-col');
      redirectToChat(card);
    });
  });

  // --- 3. HELPER: CUSTOM TOAST NOTIFICATION ---
  const showCustomToast = (message) => {
    let container = document.getElementById("custom-toast-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "custom-toast-container";
      container.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 99999;
        display: flex;
        flex-direction: column;
        gap: 10px;
      `;
      document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.style.cssText = `
      background: rgba(233, 64, 87, 0.95);
      color: white;
      padding: 12px 24px;
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(233, 64, 87, 0.3);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.25);
      font-family: 'Inter', sans-serif;
      font-size: 14px;
      font-weight: 500;
      opacity: 0;
      transform: translateY(20px);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    `;
    toast.innerText = message;
    container.appendChild(toast);

    // Trigger transition animation
    setTimeout(() => {
      toast.style.opacity = "1";
      toast.style.transform = "translateY(0)";
    }, 10);

    // Fade out and remove after 3.5s
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(20px)";
      setTimeout(() => {
        toast.remove();
      }, 300);
    }, 3500);
  };
});
