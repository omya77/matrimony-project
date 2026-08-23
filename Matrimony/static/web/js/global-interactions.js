/**
 * ForeverBond - Global Interactions Handler
 * Automatically handles dead links, action buttons, and provides premium visual feedback.
 */

document.addEventListener("DOMContentLoaded", function () {
  // Update footer social media icons to user's profiles
  document.querySelectorAll('a[aria-label="Instagram"]').forEach(el => {
    el.href = "https://www.instagram.com/omya_.x07";
    el.target = "_blank";
  });
  document.querySelectorAll('a[aria-label="Facebook"]').forEach(el => {
    el.href = "https://www.facebook.com/omkar.misal.587";
    el.target = "_blank";
  });
  document.querySelectorAll('a[aria-label="LinkedIn"]').forEach(el => {
    el.href = "https://www.linkedin.com/in/omkar-misal-aa191336b/";
    el.target = "_blank";
  });
  document.querySelectorAll('a[aria-label="YouTube"]').forEach(el => {
    el.href = "https://www.youtube.com/@OmkarMisal-ug8ks";
    el.target = "_blank";
  });

  // Inject Premium Toast Styles
  const style = document.createElement("style");
  style.textContent = `
    .sm-toast-container {
      position: fixed;
      bottom: 30px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: none;
    }
    .sm-toast {
      background: rgba(255, 255, 255, 0.9);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(233, 64, 87, 0.2);
      border-radius: 50px;
      padding: 12px 24px;
      color: #1e293b;
      font-family: 'Poppins', sans-serif;
      font-size: 14px;
      font-weight: 500;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
      display: flex;
      align-items: center;
      gap: 10px;
      opacity: 0;
      transform: translateY(20px);
      transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
    }
    .sm-toast.show {
      opacity: 1;
      transform: translateY(0);
    }
    .sm-toast.success .sm-toast-icon { color: #10b981; }
    .sm-toast.info .sm-toast-icon { color: #e94057; }
  `;
  document.head.appendChild(style);

  const toastContainer = document.createElement("div");
  toastContainer.className = "sm-toast-container";
  document.body.appendChild(toastContainer);

  window.showSmToast = function (message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `sm-toast ${type}`;
    
    let icon = type === "success" ? "fa-circle-check" : "fa-bell";
    
    toast.innerHTML = `<i class="fa-solid ${icon} sm-toast-icon" style="font-size: 18px;"></i> <span>${message}</span>`;
    toastContainer.appendChild(toast);

    // Trigger animation
    setTimeout(() => toast.classList.add("show"), 10);

    // Remove after 3 seconds
    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  };

  // Event Delegation for all clicks
  document.body.addEventListener("click", function (e) {
    // Find closest anchor or button
    let target = e.target.closest("a, button");
    if (!target) return;

    // Check if Bootstrap handles this (dropdown, modal, offcanvas, collapse, tab)
    if (target.hasAttribute("data-bs-toggle")) return;
    
    // Allow standard navigation links in navbars and menus to work normally
    if (target.closest('.navbar') || target.closest('.offcanvas') || target.closest('.dropdown-menu') || target.classList.contains('nav-link') || target.classList.contains('dropdown-item') || target.classList.contains('custom-drop-item') || target.type === 'submit' || target.closest('form')) return;

    let text = (target.textContent || "").trim().toLowerCase();
    let href = target.getAttribute("href");

    // 1. Handle Chat / Message
    if (text.includes("chat") || text.includes("message")) {
      e.preventDefault();
      window.location.href = "/interactions/chat/";
      return;
    }

    // 2. Handle Action Buttons (Connect, Send Interest, Shortlist)
    if (text.includes("connect-generic-ignore")) {
      e.preventDefault();
      if (!target.classList.contains("acted")) {
        const userId = target.getAttribute("data-user-id");
        if (userId) {
            target.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
            fetch('/interactions/api/express-interest/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ receiver_id: userId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'pending') {
                    target.innerHTML = '<i class="fa-solid fa-clock"></i> Request Sent';
                    target.style.background = "#64748b";
                    target.style.borderColor = "#64748b";
                    target.style.pointerEvents = "auto";
                    target.style.color = "#fff";
                    target.classList.add("acted");
                    showSmToast("Interest sent successfully! We will notify you once they accept.", "success");
                } else if (data.status === 'accepted') {
                    target.innerHTML = '<i class="fa-solid fa-heart"></i> Connected';
                    target.style.background = "#10b981";
                    target.style.borderColor = "#10b981";
                    target.style.color = "#fff";
                    target.classList.add("acted");
                    showSmToast("You are now connected with this user!", "success");
                } else if (data.status === 'cancelled') {
                    target.innerHTML = '<i class="fa-solid fa-heart"></i> Send Interest';
                    target.style.background = "linear-gradient(135deg, var(--rose), var(--pink))";
                    target.style.borderColor = "transparent";
                    target.style.pointerEvents = "auto";
                    target.classList.remove("acted");
                    showSmToast("Interest request cancelled.", "info");
                } else {
                    target.innerHTML = '<i class="fa-solid fa-heart"></i> Send Interest';
                    showSmToast(data.message || "Failed to send interest.", "info");
                }
            })
            .catch(err => {
                console.error("Error sending interest:", err);
                target.innerHTML = '<i class="fa-solid fa-heart"></i> Send Interest';
                showSmToast("Error sending interest. Please try again.", "info");
            });
        } else {
            // Fallback if no user id provided
            target.innerHTML = '<i class="fa-solid fa-clock"></i> Request Sent';
            target.style.background = "#64748b";
            target.style.borderColor = "#64748b";
            target.style.pointerEvents = "auto";
            target.style.color = "#fff";
            target.classList.add("acted");
            showSmToast("Interest sent successfully! We will notify you once they accept.", "success");
        }
      }
      return;
    }

    if (text.includes("shortlist") || text.includes("save")) {
      e.preventDefault();
      
      const profileId = target.getAttribute("data-profile-id");
      if (profileId) {
          if (!target.classList.contains("acted")) {
              target.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
              target.style.pointerEvents = "none";
              
              // Get CSRF token from cookies
              function getCookie(name) {
                  let cookieValue = null;
                  if (document.cookie && document.cookie !== '') {
                      const cookies = document.cookie.split(';');
                      for (let i = 0; i < cookies.length; i++) {
                          const cookie = cookies[i].trim();
                          if (cookie.substring(0, name.length + 1) === (name + '=')) {
                              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                              break;
                          }
                      }
                  }
                  return cookieValue;
              }

              fetch('/interactions/api/save-profile/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': getCookie('csrftoken')
                  },
                  body: JSON.stringify({ profile_id: profileId })
              })
              .then(response => response.json())
              .then(data => {
                  target.style.pointerEvents = "auto";
                  if (data.status === 'saved') {
                      if (target.classList.contains("mat-save-btn")) {
                          target.innerHTML = '<i class="fa-solid fa-bookmark"></i><span style="display: none;">save</span>';
                      } else {
                          target.innerHTML = '<i class="fa-solid fa-bookmark"></i> Saved';
                      }
                      target.classList.add("acted");
                      if (window.showSmToast) showSmToast("Profile saved to your shortlist.", "success");
                  } else if (data.status === 'unsaved' || data.status === 'removed') {
                      if (target.classList.contains("mat-save-btn")) {
                          target.innerHTML = '<i class="bi bi-bookmark"></i><span style="display: none;">save</span>';
                      } else {
                          target.innerHTML = '<i class="fa-solid fa-bookmark"></i> Save';
                      }
                      target.classList.remove("acted");
                      if (window.showSmToast) showSmToast("Profile removed from your shortlist.", "info");
                  } else {
                      if (target.classList.contains("mat-save-btn")) {
                          target.innerHTML = '<i class="bi bi-bookmark"></i><span style="display: none;">save</span>';
                      } else {
                          target.innerHTML = '<i class="fa-solid fa-bookmark"></i> Save';
                      }
                      if (window.showSmToast) showSmToast(data.message, 'error');
                  }
              })
              .catch(error => {
                  target.style.pointerEvents = "auto";
                  if (target.classList.contains("mat-save-btn")) {
                      target.innerHTML = '<i class="bi bi-bookmark"></i><span style="display: none;">save</span>';
                  } else {
                      target.innerHTML = '<i class="fa-solid fa-bookmark"></i> Save';
                  }
                  if (window.showSmToast) showSmToast("Failed to save profile.", "error");
              });
          } else {
              // It's already saved, let's unsave it
              target.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
              target.style.pointerEvents = "none";
              
              function getCookie(name) {
                  let cookieValue = null;
                  if (document.cookie && document.cookie !== '') {
                      const cookies = document.cookie.split(';');
                      for (let i = 0; i < cookies.length; i++) {
                          const cookie = cookies[i].trim();
                          if (cookie.substring(0, name.length + 1) === (name + '=')) {
                              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                              break;
                          }
                      }
                  }
                  return cookieValue;
              }

              fetch('/interactions/api/save-profile/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': getCookie('csrftoken')
                  },
                  body: JSON.stringify({ profile_id: profileId })
              })
              .then(response => response.json())
              .then(data => {
                  target.style.pointerEvents = "auto";
                  if (data.status === 'unsaved' || data.status === 'removed') {
                      if (target.classList.contains("mat-save-btn")) {
                          target.innerHTML = '<i class="bi bi-bookmark"></i><span style="display: none;">save</span>';
                      } else {
                          target.innerHTML = '<i class="fa-solid fa-bookmark"></i> Save';
                      }
                      target.classList.remove("acted");
                      if (window.showSmToast) showSmToast("Profile removed from your shortlist.", "info");
                  }
              });
          }
      } else {
          // Fallback for mock actions (no data-profile-id)
          if (!target.classList.contains("acted")) {
            target.innerHTML = '<i class="fa-solid fa-bookmark"></i> Saved';
            target.classList.add("acted");
            if (window.showSmToast) showSmToast("Profile saved to your shortlist.", "success");
          }
      }
      return;
    }

    // 3. Handle Read More
    if (text.includes("read more") || text.includes("view details")) {
      e.preventDefault();
      // Expand generic text if possible, else show toast
      showSmToast("Full details will be unlocked with Premium Membership.", "info");
      return;
    }

    // 4. Handle Dead Links
    if (href === "#") {
      e.preventDefault();
      showSmToast("This feature will be available soon!", "info");
      return;
    }
  });

  // Handle Form Submissions smoothly
  const forms = document.querySelectorAll("form");
  forms.forEach(form => {
    // Ignore forms that go somewhere explicitly or have action methods (except GET on #)
    let action = form.getAttribute("action");
    let method = (form.getAttribute("method") || "get").toLowerCase();
    if ((action === "#" || form.getAttribute("data-mock") === "true") && method !== "post") {
      form.addEventListener("submit", function(e) {
        e.preventDefault(); // Stop page reload
        
        // Show success loading and then toast
        let btn = form.querySelector('button[type="submit"]');
        if (btn) {
          let originalText = btn.innerHTML;
          btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
          btn.disabled = true;
          
          setTimeout(() => {
            btn.innerHTML = '<i class="fa-solid fa-check"></i> Success';
            btn.style.background = "#10b981";
            btn.style.borderColor = "#10b981";
            showSmToast("Action completed successfully!", "success");
            
            // Revert after some time
            setTimeout(() => {
              btn.innerHTML = originalText;
              btn.disabled = false;
              btn.style = "";
              form.reset();
            }, 2500);
          }, 1500);
        }
      });
    }
  });

  // Force Custom Profile Popup Toggle
  document.addEventListener("click", function(e) {
    let profileToggle = e.target.closest(".custom-user-avatar-dropdown > a");
    let insideMenu = e.target.closest(".custom-user-avatar-dropdown .dropdown-menu");
    
    // Find all custom profile dropdown menus
    let allMenus = document.querySelectorAll(".custom-user-avatar-dropdown .dropdown-menu");
    
    if (profileToggle) {
        e.preventDefault();
        e.stopPropagation();
        // Toggle the specific menu next to this anchor
        let menu = profileToggle.parentElement.querySelector(".dropdown-menu");
        if (menu) {
            let isShown = menu.classList.contains("show");
            // Close all first
            allMenus.forEach(m => { m.classList.remove("show"); m.style.display = "none"; });
            // Toggle
            if (!isShown) {
                menu.classList.add("show");
                menu.style.display = "block";
                menu.style.position = "absolute";
                menu.style.top = "100%";
                menu.style.right = "0";
                menu.style.left = "auto";
            }
        }
    } else if (!insideMenu) {
        // Clicked outside, close all
        allMenus.forEach(m => { m.classList.remove("show"); m.style.display = "none"; });
    }
  });
});
window.sendInterest = function(userId, btn) {
    if (!userId) {
        if (window.showSmToast) window.showSmToast("Please select a valid user to send interest.", "info");
        return;
    }
    let originalHtml = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';
    
    // Get CSRF token from cookies if available
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    fetch('/interactions/api/express-interest/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken || ''
        },
        body: JSON.stringify({ receiver_id: userId })
    })
    .then(response => {
        if (response.redirected && response.url.includes('/login')) {
            window.location.href = response.url;
            throw new Error('redirecting to login');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'pending') {
            btn.innerHTML = '<i class="fa-solid fa-clock"></i> Request Sent';
            btn.style.background = "#64748b";
            btn.style.pointerEvents = "auto";
            btn.classList.add("acted");
            if (window.showSmToast) window.showSmToast("Interest sent successfully!", "success");
        } else if (data.status === 'accepted') {
            btn.innerHTML = '<i class="fa-solid fa-heart"></i> Connected';
            btn.style.background = "#10b981";
            btn.classList.add("acted");
            if (window.showSmToast) window.showSmToast("You are now connected!", "success");
        } else if (data.status === 'cancelled') {
            btn.innerHTML = '<i class="fa-solid fa-heart"></i> Send Interest';
            btn.style.background = "linear-gradient(135deg, #e94057, #ff7aa2)";
            btn.style.pointerEvents = "auto";
            btn.classList.remove("acted");
            if (window.showSmToast) window.showSmToast("Interest request cancelled.", "info");
        } else {
            btn.innerHTML = originalHtml;
            if (window.showSmToast) window.showSmToast(data.message || "Failed.", "info");
        }
    })
    .catch(err => {
        btn.innerHTML = originalHtml;
        if (window.showSmToast) window.showSmToast("Error sending interest.", "info");
    });
};

window.openChat = function(userId) {
    window.location.href = "/interactions/chat/?id=" + userId;
};

// --- Track Profile Visits ---
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('show.bs.modal', function (event) {
        let modal = event.target;
        if (modal.id && modal.id.startsWith('profileModal')) {
            let userId = modal.id.replace('profileModal', '');
            
            fetch(`/interactions/api/log-visit/${userId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            }).catch(e => console.error("Error logging visit:", e));
        }
    });
});



