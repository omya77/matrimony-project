/* ==========================================================================
   FOREVERBOND Matrimony Portal Navbar, Auth, Locks & Profile Manager
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  // Sync login status and display navbar elements accordingly
  // initUserSession();

  // If user is unpaid, lock premium matches & search pages
  applyPremiumLocks();

  // Highlight active links automatically
  highlightActiveLinks();
});

// ==========================================
// 1. USER SESSION & DYNAMIC NAVBAR DROPDOWN
// ==========================================
function initUserSession() {
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
  let currentUser = null;
  try {
    currentUser = JSON.parse(localStorage.getItem("currentUser"));
  } catch (e) {
    currentUser = null;
  }

  // Update topbar actions in topbar-right
  const topbarRight = document.querySelector(".topbar-right");
  if (topbarRight) {
    if (isLoggedIn && currentUser) {
      // Create user avatar HTML
      const isPaid = localStorage.getItem("isPaid") === "true" || currentUser.isPaid === "true";
      const planName = localStorage.getItem("selectedPlan") || currentUser.planName || "Free Tier";
      const badgeHTML = isPaid 
        ? `<span class="badge text-white ms-1" style="background: linear-gradient(135deg, #e94057 0%, #facc15 100%); font-size: 8px; padding: 3px 6px;">PREMIUM (${planName})</span>` 
        : `<span class="badge bg-secondary text-white ms-1" style="font-size: 8px; padding: 3px 6px;">FREE</span>`;

      topbarRight.innerHTML = `
        <div class="lang-dropdown me-2">
          <button class="lang-btn" id="langBtn" style="background:none; border:none; color:inherit; font-size:12px; display:flex; align-items:center; gap:5px;">
            <i class="fa-solid fa-globe"></i>
            <span id="currentLanguage">English</span>
            <i class="fa-solid fa-angle-down"></i>
          </button>
          <div class="lang-menu" id="langMenu" style="display:none; position:absolute; right:0; background:white; box-shadow:0 8px 16px rgba(0,0,0,0.1); border-radius:8px; padding:5px; z-index:1000;">
            <button class="lang-item" data-lang="en" style="display:block; width:100%; border:none; background:none; text-align:left; padding:8px 12px; font-size:12px;">🇺🇸 English</button>
            <button class="lang-item" data-lang="hi" style="display:block; width:100%; border:none; background:none; text-align:left; padding:8px 12px; font-size:12px;">🇮🇳 हिन्दी</button>
            <button class="lang-item" data-lang="mr" style="display:block; width:100%; border:none; background:none; text-align:left; padding:8px 12px; font-size:12px;">🇮🇳 मराठी</button>
          </div>
        </div>
        <div class="dropdown d-inline-block">
          <a href="#" class="d-flex align-items-center gap-2 text-decoration-none dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false" style="color: #2d2033; font-weight:600; font-size:13px;">
            <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=100" alt="Avatar" class="rounded-circle border" style="width: 28px; height: 28px; object-fit:cover; border-color:#e94057 !important;" />
            <span>Hi, ${currentUser.firstName}</span>
            ${badgeHTML}
          </a>
          <ul class="dropdown-menu dropdown-menu-end border-0 shadow-lg" style="border-radius: 12px; min-width: 180px; padding: 6px; z-index:99999;">
            <li><a class="dropdown-item py-2 px-3 fw-semibold text-secondary show-profile-card-btn" href="#" style="font-size:13px; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-user-card" style="color:#e94057;"></i> View Profile</a></li>
            <li><a class="dropdown-item py-2 px-3 fw-semibold text-secondary" href="/profiles/matches/todays/" style="font-size:13px; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-gauge" style="color:#e94057;"></i> Dashboard</a></li>
            <li><a class="dropdown-item py-2 px-3 fw-semibold text-secondary" href="/payments/membership/" style="font-size:13px; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-crown" style="color:#e94057;"></i> Membership Upgrade</a></li>
            <li><hr class="dropdown-divider my-2 opacity-50" /></li>
            <li><a class="dropdown-item py-2 px-3 fw-semibold text-danger sign-out-action-btn" href="#" style="font-size:13px; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-right-from-bracket"></i> Sign Out</a></li>
          </ul>
        </div>
      `;
    } else {
      topbarRight.innerHTML = `
        <a href="/accounts/login/" class="top-btn login-btn" style="text-decoration:none; margin-right:12px; font-size:12.5px; font-weight:600; color:#555;">
          <i class="fa-solid fa-right-to-bracket me-1"></i> Login
        </a>
        <a href="/accounts/register/" class="top-btn register-btn" style="text-decoration:none; font-size:12.5px; font-weight:600; color:#555;">
          <i class="fa-solid fa-user-plus me-1"></i> Register
        </a>
      `;
    }
  }

  // Update Main Header Right side actions
  const mainHeaderRight = document.querySelector("#stickyNavWrapper .d-none.d-lg-flex.align-items-center.m-0");
  const matchesHeaderRight = document.querySelector("#stickyNavWrapper .d-none.d-lg-flex.align-items-center.gap-4.m-0.p-0");
  const activeHeaderContainer = mainHeaderRight || matchesHeaderRight;

  if (activeHeaderContainer) {
    if (isLoggedIn && currentUser) {
      const isPaid = localStorage.getItem("isPaid") === "true" || currentUser.isPaid === "true";
      const planName = localStorage.getItem("selectedPlan") || currentUser.planName || "Free Tier";
      const planHTML = isPaid 
        ? `<span class="d-flex align-items-center gap-1" style="font-size: 9px; font-weight: 800; color: #facc15; letter-spacing: 0.3px;"><i class="fa-solid fa-crown" style="font-size: 8px;"></i> PREMIUM (${planName})</span>`
        : `<span class="d-flex align-items-center gap-1" style="font-size: 9px; font-weight: 800; color: #64748b; letter-spacing: 0.3px;"><i class="fa-solid fa-circle-info" style="font-size: 8px;"></i> FREE STANDARD</span>`;

      // Use user uploaded photo if available, else fallback
      const profilePhoto = localStorage.getItem("profilePhoto") || "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=100";

      activeHeaderContainer.innerHTML = `
            <!-- Notification Center -->
            <div class="dropdown custom-notification-dropdown d-inline-block">
  <a href="javascript:void(0)" class="position-relative text-decoration-none transition-all hover-scale d-inline-block py-1 dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false" role="button">
    <i class="fa-solid fa-bell" style="color: #64748b; font-size: 19px"></i>
    <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style="font-size: 9px; padding: 3px 5px; background-color: #e94057 !important;">3</span>
  </a>
  <div class="dropdown-menu dropdown-menu-end shadow-lg border-0 p-0" style="width: 320px; max-width: 90vw; border-radius: 16px; margin-top: 15px; z-index: 1050; overflow: hidden;">
    <div class="p-3 border-bottom d-flex justify-content-between align-items-center" style="background: #f8fafc;">
      <h6 class="m-0" style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #1e293b;">Notifications</h6>
      <span class="badge" style="background: #e94057; font-size: 10px;">3 New</span>
    </div>
    <div class="notification-list" style="max-height: 300px; overflow-y: auto;">
      <a href="#" class="dropdown-item d-flex align-items-start gap-3 p-3 border-bottom text-wrap" style="white-space: normal;">
        <div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px; background: rgba(233, 64, 87, 0.1); color: #e94057;">
          <i class="fa-solid fa-heart"></i>
        </div>
        <div>
          <p class="m-0" style="font-size: 13px; color: #334155; font-weight: 500;"><strong>Priya Sharma</strong> accepted your match request!</p>
          <span style="font-size: 11px; color: #94a3b8;">2 hours ago</span>
        </div>
      </a>
      <a href="#" class="dropdown-item d-flex align-items-start gap-3 p-3 border-bottom text-wrap" style="white-space: normal;">
        <div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px; background: rgba(250, 204, 21, 0.1); color: #facc15;">
          <i class="fa-solid fa-crown"></i>
        </div>
        <div>
          <p class="m-0" style="font-size: 13px; color: #334155; font-weight: 500;">Your Premium membership is expiring soon.</p>
          <span style="font-size: 11px; color: #94a3b8;">5 hours ago</span>
        </div>
      </a>
      <a href="#" class="dropdown-item d-flex align-items-start gap-3 p-3 text-wrap" style="white-space: normal;">
        <div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px; background: rgba(14, 165, 233, 0.1); color: #0ea5e9;">
          <i class="fa-solid fa-eye"></i>
        </div>
        <div>
          <p class="m-0" style="font-size: 13px; color: #334155; font-weight: 500;"><strong>Rahul Verma</strong> viewed your profile.</p>
          <span style="font-size: 11px; color: #94a3b8;">1 day ago</span>
        </div>
      </a>
    </div>
    <div class="p-2 text-center border-top" style="background: #f8fafc;">
      <a href="#" class="text-decoration-none" style="font-size: 13px; font-weight: 600; color: #e94057;">View All Notifications</a>
    </div>
  </div>
</div>

        <!-- Upgrade Button -->
        <a href="/payments/membership/" class="btn ultimate-action-btn d-flex align-items-center gap-2" style="font-size:12px; padding: 8px 18px !important; border-radius:999px;">
          <i class="fa-solid fa-crown" style="font-size: 11px; color: #facc15"></i>
          <span>${isPaid ? 'MY PLAN' : 'UPGRADE'}</span>
        </a>
        
        <!-- User Profile Dropdown System -->
        <div class="dropdown custom-user-avatar-dropdown position-relative">
          <a href="javascript:void(0)" class="d-flex align-items-center gap-2 text-decoration-none dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false" role="button" style="cursor: pointer;">
            <div class="position-relative" style="width: 38px; height: 38px; flex-shrink: 0">
              <img src="${profilePhoto}" alt="User Profile" class="rounded-circle border" style="width: 38px; height: 38px; object-fit: cover; border-color: rgba(233, 64, 87, 0.4) !important; padding: 1.5px;" />
              <span class="position-absolute bottom-0 end-0 bg-success border border-white rounded-circle" style="width: 10px; height: 10px"></span>
            </div>
            <div class="d-flex flex-column text-start justify-content-center" style="max-width: 100px">
              <span style="font-size: 13px; font-weight: 700; color: #1e293b; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Hi, ${currentUser.firstName}</span>
              ${planHTML}
            </div>
          </a>
          <div class="dropdown-menu dropdown-menu-end shadow-lg border-0 p-4" style="width: 280px; max-width: 90vw; border-radius: 20px; background: #ffffff; margin-top: 15px; z-index: 1050;">
              <div class="text-center">
                  <div class="position-relative d-inline-block mb-3">
                      <img src="${profilePhoto}" alt="User" class="rounded-circle" style="width: 80px; height: 80px; object-fit: cover; border: 3px solid #fff; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                      <span class="position-absolute bottom-0 end-0 bg-success border border-white rounded-circle" style="width: 15px; height: 15px; transform: translate(-10px, -5px);"></span>
                  </div>
                  <h5 style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #1e293b; margin-bottom: 5px;">${currentUser.firstName} ${currentUser.lastName || ''}</h5>
                  <p style="font-size: 13px; color: #64748b; line-height: 1.5; margin-bottom: 15px;">
                      ${currentUser.email || ''}<br>
                      <span class="badge bg-danger text-white mt-1">Profile ID: FB${Math.floor(100000 + Math.random() * 900000)}</span>
                  </p>
                  <a href="/profiles/my-profile-data/" class="btn text-white w-100 rounded-pill py-2" style="background: #a16238; font-weight: 600; font-size: 14px; border: none; box-shadow: 0 4px 10px rgba(161, 98, 56, 0.3);">
                      View your Profile
                  </a>
              </div>
              
              <hr style="opacity: 0.1; margin: 20px 0 10px;">
              
              <div class="d-flex flex-column gap-1" style="font-size: 14px;">
                  <a href="/profiles/saved-profiles/" class="dropdown-item d-flex align-items-center gap-3 rounded py-2" style="color: #475569; font-weight: 500;">
                      <i class="fa-solid fa-bookmark" style="font-size: 16px; color: #94a3b8; width: 20px; text-align: center;"></i> Saved Profiles
                  </a>
                  <a href="/interactions/requests/" class="dropdown-item d-flex align-items-center gap-3 rounded py-2" style="color: #475569; font-weight: 500;">
                      <i class="fa-solid fa-user-group" style="font-size: 16px; color: #94a3b8; width: 20px; text-align: center;"></i> Connection Manager
                  </a>
                  <a href="/payments/billing/" class="dropdown-item d-flex align-items-center gap-3 rounded py-2" style="color: #475569; font-weight: 500;">
                      <i class="fa-solid fa-file-invoice" style="font-size: 16px; color: #94a3b8; width: 20px; text-align: center;"></i> Billing & Invoices
                  </a>
                  <a href="/accounts/settings/" class="dropdown-item d-flex align-items-center gap-3 rounded py-2" style="color: #475569; font-weight: 500;">
                      <i class="fa-solid fa-gear" style="font-size: 16px; color: #94a3b8; width: 20px; text-align: center;"></i> Settings
                  </a>
                  <a href="/" class="dropdown-item d-flex align-items-center gap-3 rounded py-2" style="color: #475569; font-weight: 500;">
                      <i class="fa-solid fa-right-from-bracket" style="font-size: 16px; color: #e94057; width: 20px; text-align: center;"></i> Sign out
                  </a>
              </div>
          </div>
        </div>
      `;
    } else {
      activeHeaderContainer.innerHTML = `
        <a href="/payments/membership/" class="btn ultimate-action-btn d-flex align-items-center gap-2" style="font-size:12px; padding: 8px 18px !important; border-radius:999px;">
          <i class="fa-solid fa-crown" style="font-size: 11px; color: #facc15"></i>
          <span>MEMBERSHIP</span>
        </a>
      `;
    }
  }

  // DYNAMIC MENU INJECTION (Desktop .navbar-nav & Mobile Menu List)
  const desktopNav = document.querySelector(".navbar-nav");
  const mobileNavList = document.querySelector("#mobileOffcanvas .offcanvas-body ul.flex-column") || document.getElementById("mobileNavList");

  if (isLoggedIn && currentUser) {
    // 1. Desktop Logged In Full Menu
    if (desktopNav) {
      desktopNav.innerHTML = `
        <li class="nav-item">
          <a href="/" class="nav-link ultra-nav-link">
            <i class="fa-solid fa-house"></i> <span>HOME</span>
          </a>
        </li>
        
        <!-- SEARCH DROPDOWN -->
        <li class="nav-item dropdown custom-premium-dropdown">
          <a href="#" class="nav-link ultra-nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false">
            <i class="fa-solid fa-magnifying-glass"></i> <span>SEARCH</span>
          </a>
          <ul class="dropdown-menu border-0 shadow-lg dynamic-glass-dropdown" style="background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border-radius: 16px; padding: 8px; border: 1px solid rgba(233, 64, 87, 0.1) !important; margin-top: 10px;">
            <li><a class="dropdown-item custom-drop-item" href="/profiles/search/basic/"><i class="fa-solid fa-list-check" style="color: #e94057"></i> Basic Search</a></li>
            <li><a class="dropdown-item custom-drop-item" href="/profiles/search/advanced/"><i class="fa-solid fa-sliders" style="color: #e94057"></i> Advance Search</a></li>
            <li><a class="dropdown-item custom-drop-item" href="/profiles/search/ai/"><i class="fa-solid fa-brain" style="color: #e94057"></i> AI Match Finder</a></li>
            <li><a class="dropdown-item custom-drop-item" href="/profiles/search/saved/"><i class="fa-solid fa-bookmark" style="color: #e94057"></i> Saved Searches</a></li>
          </ul>
        </li>

        <!-- MATCHES DROPDOWN -->
        <li class="nav-item dropdown custom-premium-dropdown">
          <a href="#" class="nav-link ultra-nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false">
            <i class="fa-solid fa-heart-pulse"></i> <span>MATCHES</span>
          </a>
          <ul class="dropdown-menu border-0 shadow-lg dynamic-glass-dropdown" style="background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border-radius: 16px; padding: 8px; border: 1px solid rgba(233, 64, 87, 0.1) !important; margin-top: 10px;">
            <li><a class="dropdown-item custom-drop-item" href="/profiles/matches/todays/"><i class="fa-solid fa-calendar-day" style="color: #e94057"></i> Today's Matches</a></li>
            <li><a class="dropdown-item custom-drop-item" href="/profiles/matches/recommended/"><i class="fa-solid fa-star" style="color: #e94057"></i> Recommended Matches</a></li>
            <li><a class="dropdown-item custom-drop-item" href="/profiles/matches/ai-match/"><i class="fa-solid fa-wand-magic-sparkles" style="color: #e94057"></i> AI Matches</a></li>
            <li><a class="dropdown-item custom-drop-item" href="/profiles/matches/nearby/"><i class="fa-solid fa-location-dot" style="color: #e94057"></i> Nearby Matches</a></li>
          </ul>
        </li>

        <!-- PROFILES DROPDOWN -->
        <li class="nav-item dropdown custom-premium-dropdown">
          <a href="#" class="nav-link ultra-nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false">
            <i class="fa-solid fa-users"></i> <span>PROFILES</span>
          </a>
          <ul class="dropdown-menu border-0 shadow-lg dynamic-glass-dropdown" style="background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border-radius: 16px; padding: 8px; border: 1px solid rgba(233, 64, 87, 0.1) !important; margin-top: 10px;">
            <li><a class="dropdown-item custom-drop-item" href="/profiles/featured/brides/"><i class="fa-solid fa-person-dress" style="color: #e94057"></i> Featured Brides</a></li>
            <li><a class="dropdown-item custom-drop-item" href="/profiles/featured/grooms/"><i class="fa-solid fa-person" style="color: #e94057"></i> Featured Grooms</a></li>
            <li><a class="dropdown-item custom-drop-item" href="/profiles/verified-profiles/"><i class="fa-solid fa-user-shield" style="color: #e94057"></i> Verified Profiles</a></li>
            <li><a class="dropdown-item custom-drop-item" href="/profiles/saved-profiles/"><i class="fa-solid fa-folder-heart" style="color: #e94057"></i> Saved Profiles</a></li>
          </ul>
        </li>

        ${!isPaid ? `
        <li class="nav-item">
          <a href="/stories/" class="nav-link ultra-nav-link">
            <i class="fa-solid fa-bell-concierge"></i> <span>STORIES</span>
          </a>
        </li>

        <!-- BLOG DROPDOWN -->
        <li class="nav-item dropdown custom-premium-dropdown">
          <a href="#" class="nav-link ultra-nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false">
            <i class="fa-solid fa-newspaper"></i> <span>BLOG</span>
          </a>
          <ul class="dropdown-menu border-0 shadow-lg dynamic-glass-dropdown" style="background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border-radius: 16px; padding: 8px; border: 1px solid rgba(233, 64, 87, 0.1) !important; margin-top: 10px;">
            <li><a class="dropdown-item custom-drop-item" href="/latest-article/"><i class="fa-solid fa-book-open" style="color: #e94057"></i> Latest Articles</a></li>
            <li><a class="dropdown-item custom-drop-item" href="/relationship-tips/"><i class="fa-solid fa-handshake" style="color: #e94057"></i> Relationship Tips</a></li>
            <li><a class="dropdown-item custom-drop-item" href="/marriage-advice/"><i class="fa-solid fa-ring" style="color: #e94057"></i> Marriage Advice</a></li>
          </ul>
        </li>

        <li class="nav-item">
          <a href="/contact/" class="nav-link ultra-nav-link">
            <i class="fa-solid fa-envelope"></i> <span>CONTACT</span>
          </a>
        </li>
        ` : ''}
      `;
    }

    // 2. Mobile Logged In Full Menu
    if (mobileNavList) {
      mobileNavList.innerHTML = `
        <li class="nav-item">
          <a href="/" class="nav-link mobile-nav-link" style="font-size:14px; font-weight:700; color:#475569; padding:8px 16px; display:flex; align-items:center; gap:10px; text-decoration:none;">
            <i class="fa-solid fa-house" style="color:#e94057; width:18px;"></i> HOME
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link mobile-nav-link d-flex justify-content-between align-items-center" data-bs-toggle="collapse" href="#mobileSearchCollapse" role="button" aria-expanded="false" style="font-size:14px; font-weight:700; color:#475569; padding:8px 16px; text-decoration:none;">
            <span><i class="fa-solid fa-magnifying-glass" style="color:#e94057; width:18px;"></i> SEARCH</span>
            <i class="fa-solid fa-chevron-down ms-auto" style="font-size: 10px"></i>
          </a>
          <div class="collapse ps-3 mt-1" id="mobileSearchCollapse">
            <ul class="nav flex-column gap-1" style="border-left: 1px dashed rgba(233, 64, 87, 0.3); padding-left: 10px;">
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/profiles/search/basic/"><i class="fa-solid fa-list-check"></i> Basic Search</a></li>
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/profiles/search/advanced/"><i class="fa-solid fa-sliders"></i> Advance Search</a></li>
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/profiles/search/ai/"><i class="fa-solid fa-brain"></i> AI Match Finder</a></li>
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/profiles/search/saved/"><i class="fa-solid fa-bookmark"></i> Saved Searches</a></li>
            </ul>
          </div>
        </li>
        <li class="nav-item">
          <a class="nav-link mobile-nav-link d-flex justify-content-between align-items-center" data-bs-toggle="collapse" href="#mobileMatchesCollapse" role="button" aria-expanded="false" style="font-size:14px; font-weight:700; color:#475569; padding:8px 16px; text-decoration:none;">
            <span><i class="fa-solid fa-heart-pulse" style="color:#e94057; width:18px;"></i> MATCHES</span>
            <i class="fa-solid fa-chevron-down ms-auto" style="font-size: 10px"></i>
          </a>
          <div class="collapse ps-3 mt-1" id="mobileMatchesCollapse">
            <ul class="nav flex-column gap-1" style="border-left: 1px dashed rgba(233, 64, 87, 0.3); padding-left: 10px;">
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/profiles/matches/todays/"><i class="fa-solid fa-calendar-day"></i> Today's Matches</a></li>
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/profiles/matches/recommended/"><i class="fa-solid fa-star"></i> Recommended Matches</a></li>
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/profiles/matches/ai-match/"><i class="fa-solid fa-wand-magic-sparkles"></i> AI Matches</a></li>
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/profiles/matches/nearby/"><i class="fa-solid fa-location-dot"></i> Nearby Matches</a></li>
            </ul>
          </div>
        </li>
        <li class="nav-item">
          <a class="nav-link mobile-nav-link d-flex justify-content-between align-items-center" data-bs-toggle="collapse" href="#mobileProfilesCollapse" role="button" aria-expanded="false" style="font-size:14px; font-weight:700; color:#475569; padding:8px 16px; text-decoration:none;">
            <span><i class="fa-solid fa-users" style="color:#e94057; width:18px;"></i> PROFILES</span>
            <i class="fa-solid fa-chevron-down ms-auto" style="font-size: 10px"></i>
          </a>
          <div class="collapse ps-3 mt-1" id="mobileProfilesCollapse">
            <ul class="nav flex-column gap-1" style="border-left: 1px dashed rgba(233, 64, 87, 0.3); padding-left: 10px;">
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/profiles/featured/brides/"><i class="fa-solid fa-person-dress"></i> Featured Brides</a></li>
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/profiles/featured/grooms/"><i class="fa-solid fa-person"></i> Featured Grooms</a></li>
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/profiles/verified-profiles/"><i class="fa-solid fa-user-shield"></i> Verified Profiles</a></li>
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/profiles/saved-profiles/"><i class="fa-solid fa-folder-heart"></i> Saved Profiles</a></li>
            </ul>
          </div>
        </li>

        ${!isPaid ? `
        <li class="nav-item">
          <a href="/stories/" class="nav-link mobile-nav-link" style="font-size:14px; font-weight:700; color:#475569; padding:8px 16px; display:flex; align-items:center; gap:10px; text-decoration:none;">
            <i class="fa-solid fa-bell-concierge" style="color:#e94057; width:18px;"></i> STORIES
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link mobile-nav-link d-flex justify-content-between align-items-center" data-bs-toggle="collapse" href="#mobileBlogCollapse" role="button" aria-expanded="false" style="font-size:14px; font-weight:700; color:#475569; padding:8px 16px; text-decoration:none;">
            <span><i class="fa-solid fa-newspaper" style="color:#e94057; width:18px;"></i> BLOG</span>
            <i class="fa-solid fa-chevron-down ms-auto" style="font-size: 10px"></i>
          </a>
          <div class="collapse ps-3 mt-1" id="mobileBlogCollapse">
            <ul class="nav flex-column gap-1" style="border-left: 1px dashed rgba(233, 64, 87, 0.3); padding-left: 10px;">
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/latest-article/"><i class="fa-solid fa-book-open"></i> Latest Articles</a></li>
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/relationship-tips/"><i class="fa-solid fa-handshake"></i> Relationship Tips</a></li>
              <li><a class="nav-link mobile-nav-link py-1.5" style="font-size: 13px; text-decoration:none;" href="/marriage-advice/"><i class="fa-solid fa-ring"></i> Marriage Advice</a></li>
            </ul>
          </div>
        </li>
        <li class="nav-item">
          <a href="/contact/" class="nav-link mobile-nav-link" style="font-size:14px; font-weight:700; color:#475569; padding:8px 16px; display:flex; align-items:center; gap:10px; text-decoration:none;">
            <i class="fa-solid fa-envelope" style="color:#e94057; width:18px;"></i> CONTACT
          </a>
        </li>
        ` : ''}
      `;
    }
  }

  // Update mobile drawer user info header block
  const mobileLabel = document.getElementById("mobileOffcanvasLabel");
  const mobileDrawerHeader = mobileLabel ? mobileLabel.parentElement : null;
  if (isLoggedIn && currentUser && mobileDrawerHeader) {
    mobileDrawerHeader.innerHTML = `
      <div class="d-flex align-items-center gap-2.5">
        <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=100" alt="User" class="rounded-circle border" style="width: 35px; height: 35px; object-fit: cover; border-color: #e94057 !important;" />
        <h5 class="offcanvas-title m-0" id="mobileOffcanvasLabel" style="font-family: 'Poppins', sans-serif; font-weight:800; font-size:16px; color:#1e293b;">
          ${currentUser.firstName} <span style="color: #e94057">${currentUser.lastName}</span>
        </h5>
      </div>
      <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close" style="box-shadow: none"></button>
    `;

    // Add profile card triggers and signout to mobile list if not already present
    if (mobileNavList && !document.getElementById("mobileAuthSec")) {
      const authSec = document.createElement("div");
      authSec.id = "mobileAuthSec";
      authSec.className = "w-100 mt-3 pt-3 border-top border-light";
      authSec.innerHTML = `
        <button class="btn w-100 text-start mobile-nav-link show-profile-card-btn" style="border:none; background:none; padding:12px 16px;"><i class="fa-solid fa-user" style="color:#e94057; width:18px;"></i> My Profile Card</button>
        <button class="btn w-100 text-start mobile-nav-link sign-out-action-btn" style="border:none; background:none; padding:12px 16px; color:#dc3545 !important;"><i class="fa-solid fa-right-from-bracket" style="color:#dc3545; width:18px;"></i> Sign Out</button>
      `;
      mobileNavList.appendChild(authSec);
    }
  }

  // Bind Sign Out action
  document.querySelectorAll(".sign-out-action-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.removeItem("isLoggedIn");
      localStorage.removeItem("currentUser");
      localStorage.removeItem("isPaid");
      localStorage.removeItem("selectedPlan");
      alert("🔒 Logged out successfully!");
      window.location.href = "/home/";
    });
  });

  // Bind Profile Card action
  document.querySelectorAll(".show-profile-card-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      openUserProfileCardModal();
    });
  });

  // Language Dropdown open logic
  const langBtnNode = document.getElementById("langBtn");
  const langMenuNode = document.getElementById("langMenu");
  if (langBtnNode && langMenuNode) {
    langBtnNode.addEventListener("click", (e) => {
      e.stopPropagation();
      langMenuNode.style.display = langMenuNode.style.display === "block" ? "none" : "block";
    });
    document.addEventListener("click", () => {
      langMenuNode.style.display = "none";
    });
  }
}

// ==========================================
// 2. LOCK FEATURE FOR UNPAID USERS
// ==========================================
function applyPremiumLocks() {
  const isPaid = localStorage.getItem("isPaid") === "true";

  // List of paths that require active premium membership
  const premiumPaths = [
    "/profiles/matches/todays/",
    "/profiles/matches/recommended/",
    "/profiles/matches/ai-match/",
    "/profiles/matches/nearby/",
    "/profiles/featured/brides/",
    "/profiles/featured/grooms/",
    "/profiles/verified-profiles/",
    "/profiles/saved-profiles/",
    "/profiles/search/basic/",
    "/profiles/search/advanced/",
    "/profiles/search/ai/",
    "/profiles/search/saved/"
  ];

  const currentPath = window.location.pathname;

  // If user is unpaid and opens a premium page, lock the page
  if (premiumPaths.includes(currentPath) && !isPaid) {
    // Lock overlay markup injection
    const overlay = document.createElement("div");
    overlay.id = "premium-lock-overlay";
    overlay.style.cssText = `
      position: fixed;
      inset: 0;
      z-index: 99999;
      background: rgba(30, 20, 35, 0.72);
      backdrop-filter: blur(25px);
      -webkit-backdrop-filter: blur(25px);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Inter', sans-serif;
    `;

    overlay.innerHTML = `
      <div style="background: white; border-radius: 28px; width: 90%; max-width: 480px; padding: 40px 30px; text-align: center; box-shadow: 0 25px 60px rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.7); animation: modalZoom 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);">
        <style>
          @keyframes modalZoom {
            from { opacity: 0; transform: scale(0.9) translateY(20px); }
            to { opacity: 1; transform: scale(1) translateY(0); }
          }
        </style>
        <div style="width: 80px; height: 80px; background: #fff1f3; color: #e94057; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 38px; margin-bottom: 24px; box-shadow: 0 8px 24px rgba(233, 64, 87, 0.15);">
          <i class="fa-solid fa-lock"></i>
        </div>
        <h3 style="font-family: 'Poppins', sans-serif; font-weight:800; color: #2d2033; margin-bottom: 12px; font-size: 22px;">🔒 Premium Matrimony Feature</h3>
        <p style="font-size: 14px; color: #64748b; line-height: 1.6; margin-bottom: 30px;">
          Matching profiles, search features, and member directory details are locked for standard accounts. Subscribe to a membership plan to unlock verified matches and start your journey.
        </p>
        <div style="display:flex; flex-direction:column; gap:12px;">
          <a href="/payments/membership/" style="padding: 12px 25px; border-radius: 25px; background: linear-gradient(135deg, #e94057 0%, #fd5e53 100%); color: white; font-weight: 700; font-size: 14.5px; text-decoration: none; display:block; box-shadow: 0 8px 20px rgba(233, 64, 87, 0.25); transition:all 0.25s;">
            <i class="fa-solid fa-crown" style="color: #facc15; margin-right:6px;"></i> View Membership Plans
          </a>
          <a href="/home/" style="padding: 11px 25px; border-radius: 25px; background: #f1f5f9; color: #475569; font-weight: 700; font-size: 14px; text-decoration: none; display:block; border: 1px solid #e2e8f0; transition:all 0.25s;">
            Back to Home
          </a>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);
    document.body.style.overflow = "hidden"; // disable background scrolling
  }

  // Lock style indicator additions to navbar dropdown links
  if (!isPaid) {
    document.querySelectorAll(".custom-drop-item").forEach(item => {
      const hrefVal = item.getAttribute("href");
      if (premiumPaths.includes(hrefVal)) {
        // Append padlock lock icon next to link text
        if (!item.querySelector(".navbar-lock-badge")) {
          const lockBadge = document.createElement("i");
          lockBadge.className = "fa-solid fa-lock navbar-lock-badge ms-auto";
          lockBadge.style.cssText = "color:#facc15; font-size: 10px; opacity:0.85;";
          item.appendChild(lockBadge);
        }
      }
    });
  }
}

// ==========================================
// 3. USER PROFILE BIODATA CARD MODAL
// ==========================================
function openUserProfileCardModal() {
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
  let currentUser = null;
  try {
    currentUser = JSON.parse(localStorage.getItem("currentUser"));
  } catch (e) {
    currentUser = null;
  }

  if (!isLoggedIn || !currentUser) {
    alert("🔒 Please log in first.");
    window.location.href = "/accounts/login/";
    return;
  }

  const isPaid = localStorage.getItem("isPaid") === "true" || currentUser.isPaid === "true";
  const planName = localStorage.getItem("selectedPlan") || currentUser.planName || "Free Tier";

  // Create Modal element if not already exists
  let profileModal = document.getElementById("profile-details-modal");
  if (!profileModal) {
    profileModal = document.createElement("div");
    profileModal.id = "profile-details-modal";
    profileModal.style.cssText = `
      position: fixed;
      inset: 0;
      z-index: 999999;
      background: rgba(30, 20, 35, 0.7);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Inter', sans-serif;
    `;
    document.body.appendChild(profileModal);
  }

  // Calculate dynamic parameters
  const dobVal = new Date(currentUser.dob || "1998-05-15");
  const age = new Date().getFullYear() - dobVal.getFullYear();
  const regId = "FB" + (dobVal.getTime().toString().substring(7, 13) || "928372");

  // Use user uploaded photo if available
  const profilePhotoSrc = localStorage.getItem("profilePhoto") || "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=120";

  profileModal.innerHTML = `
    <div style="background: white; border-radius: 28px; width: 95%; max-width: 580px; padding: 0; box-shadow: 0 30px 70px rgba(233, 64, 87, 0.2); border: 1px solid rgba(233, 64, 87, 0.15); overflow: hidden; position: relative; animation: modalSlideUp 0.35s cubic-bezier(0.165, 0.84, 0.44, 1);">
      <style>
        @keyframes modalSlideUp {
          from { opacity: 0; transform: translateY(40px) scale(0.97); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .profile-row-info {
          display: flex;
          justify-content: space-between;
          border-bottom: 1px solid #f1f5f9;
          padding: 12px 16px;
          font-size: 13.5px;
        }
        .profile-row-info span { color: #64748b; font-weight: 500; }
        .profile-row-info strong { color: #1e293b; font-weight: 700; }
      </style>
      
      <!-- Premium Glass header banner -->
      <div style="background: linear-gradient(135deg, #e94057 0%, #fd5e53 100%); padding: 30px 24px; color: white; position: relative; text-align: center;">
        <button id="close-profile-modal-btn" style="position: absolute; right: 18px; top: 18px; background: none; border: none; font-size: 22px; color: white; cursor: pointer; opacity: 0.85; transition: opacity 0.2s;">
          <i class="fa-solid fa-xmark"></i>
        </button>
        
        <!-- Profile Avatar container -->
        <div style="position: relative; width: 100px; height: 100px; margin: 0 auto 12px; border-radius: 50%; box-shadow: 0 8px 24px rgba(0,0,0,0.2);">
          <img src="${profilePhotoSrc}" alt="Profile avatar" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 4px solid white;" />
          <span style="position: absolute; bottom: 0; right: 0; background: #facc15; border: 2px solid white; color: #2d2033; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; box-shadow: 0 3px 6px rgba(0,0,0,0.15);" title="Verified Profile">
            <i class="fa-solid fa-check"></i>
          </span>
        </div>
        
        <h3 style="font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 22px; margin-bottom: 4px; letter-spacing: -0.3px;">
          ${currentUser.firstName} ${currentUser.lastName}
        </h3>
        <span style="font-size: 11.5px; opacity: 0.9; letter-spacing: 0.5px; font-weight: 500;">Matrimony ID: ${regId} | ${currentUser.gender}</span>
        
        <!-- Membership Badge overlay -->
        <div style="margin-top: 12px;">
          <span style="background: rgba(255,255,255,0.2); border: 1.5px solid rgba(255,255,255,0.4); border-radius: 20px; padding: 4px 18px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; display: inline-flex; align-items: center; gap: 6px; text-transform: uppercase;">
            <i class="fa-solid fa-crown" style="color: #facc15;"></i> ${planName} Plan Active
          </span>
        </div>
      </div>
      
      <!-- Body details listing -->
      <div style="padding: 24px 20px;">
        <h5 style="font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 14.5px; color: #e94057; margin-bottom: 12px; padding-left: 8px;">
          <i class="fa-solid fa-address-card me-1"></i> Personal Profile Biodata Card
        </h5>
        <div style="background: #fafafa; border-radius: 16px; border: 1px solid #f1f5f9; overflow: hidden; margin-bottom: 24px;">
          <div class="profile-row-info">
            <span>First Name</span>
            <strong>${currentUser.firstName}</strong>
          </div>
          <div class="profile-row-info">
            <span>Last Name</span>
            <strong>${currentUser.lastName}</strong>
          </div>
          <div class="profile-row-info">
            <span>Gender / Age</span>
            <strong>${currentUser.gender} / ${age} Years</strong>
          </div>
          <div class="profile-row-info">
            <span>Date of Birth</span>
            <strong>${dobVal.toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' })}</strong>
          </div>
          <div class="profile-row-info">
            <span>Mobile Contact</span>
            <strong>${currentUser.mobile}</strong>
          </div>
          <div class="profile-row-info">
            <span>Email Address</span>
            <strong>${currentUser.email}</strong>
          </div>
          <div class="profile-row-info">
            <span>Membership Status</span>
            <strong style="color: ${isPaid ? '#10b981' : '#64748b'}">${isPaid ? 'Premium Verified' : 'Standard Basic'}</strong>
          </div>
        </div>
        
        <div style="display:flex; gap:12px; justify-content:flex-end;">
          <button id="edit-profile-dummy-btn" style="padding: 10px 24px; border-radius: 20px; background: #e94057; border: none; color: white; font-weight: 700; font-size: 13.5px; cursor: pointer; box-shadow: 0 4px 10px rgba(233, 64, 87, 0.2); transition: all 0.2s;" onclick="alert('Redirecting to Edit Profile section...')">Edit Details</button>
          <button id="close-profile-btn" style="padding: 10px 24px; border-radius: 20px; background: #f1f5f9; border: 1px solid #e2e8f0; color: #475569; font-weight: 700; font-size: 13.5px; cursor: pointer; transition: all 0.2s;">Close</button>
        </div>
      </div>
    </div>
  `;

  // Bind close buttons
  document.getElementById("close-profile-modal-btn").addEventListener("click", () => {
    profileModal.style.display = "none";
  });
  document.getElementById("close-profile-btn").addEventListener("click", () => {
    profileModal.style.display = "none";
  });
}

// ==========================================
// 4. HIGHLIGHT ACTIVE NAV LINK AUTOMATICALLY
// ==========================================
function highlightActiveLinks() {
  const activePage = window.location.pathname;

  // Process top desktop menu links
  document.querySelectorAll(".ultra-nav-link").forEach(link => {
    const href = link.getAttribute("href");
    if (href === activePage || (activePage === "/home/" && href === "/")) {
      link.classList.add("active-premium-link");
    } else {
      link.classList.remove("active-premium-link");
    }
  });

  // Process mobile accordion links
  document.querySelectorAll(".mobile-nav-link").forEach(link => {
    const href = link.getAttribute("href");
    if (href === activePage || (activePage === "/home/" && href === "/")) {
      link.classList.add("active-mobile");
      const collapse = link.closest(".collapse");
      if (collapse) {
        collapse.classList.add("show");
        const toggler = document.querySelector(`[href="#${collapse.id}"]`);
        if (toggler) toggler.classList.add("active-mobile");
      }
    }
  });
}

