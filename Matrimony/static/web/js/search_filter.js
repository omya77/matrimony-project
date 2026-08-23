/* ==========================================================================
   MATRIMONY PORTAL CLIENT-SIDE SEARCH FILTER ENGINE (search_filter.js)
   Updated with strict gender filtering and modern FormData matching
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  const searchForm = document.querySelector(".filter-card form") || document.querySelector(".pm-filter-card form") || document.querySelector("form.search-form") || document.querySelector("form");
  if (!searchForm) return;

  // Simple heuristic lists for dummy data filtering
  const femaleKeywords = ["snehal", "priya", "riya", "anjali", "neha", "pooja", "shreya", "aarti", "kavita", "swati", "nisha", "ehadiyen"];
  const maleKeywords = ["rahul", "rohit", "amit", "vikas", "sachin", "manish", "sunil", "anil", "vijay", "sanjay", "ajay"];

  searchForm.addEventListener("submit", (e) => {
    e.preventDefault();
    
    // Grab all form data via modern FormData API (works because we added 'name' attributes)
    const formData = new FormData(searchForm);
    
    let lookingFor = (formData.get("gender") || formData.get("looking_for") || "").toLowerCase().trim();
    let ageFrom = parseInt(formData.get("age_min") || formData.get("age-from") || 18);
    let ageTo = parseInt(formData.get("age_max") || formData.get("age-to") || 100);
    let religion = (formData.get("religion") || "").toLowerCase().trim();
    let motherTongue = (formData.get("mother_tongue") || formData.get("tongue") || "").toLowerCase().trim();
    let location = (formData.get("city") || formData.get("state") || formData.get("country") || "").toLowerCase().trim();

    // Query card list
    const cards = document.querySelectorAll(".profile-container .glass-card, .pm-profile-container .pm-profile-card, .profile-card-dark");
    let matchedCount = 0;

    cards.forEach(card => {
      const detailsText = card.textContent.toLowerCase();
      
      // Extract Age from card
      const ageMatch = detailsText.match(/age:\s*(\d+)/i) || detailsText.match(/\b(\d+)\s*•/);
      const age = ageMatch ? parseInt(ageMatch[1]) : null;

      let matches = true;

      // 1. Gender Filter (Ladka / Ladki logic based on dummy data heuristic)
      if (lookingFor && lookingFor !== "any" && lookingFor !== "select...") {
        let isLookingForBride = lookingFor.includes("bride") || lookingFor.includes("female") || lookingFor === "f";
        let isLookingForGroom = lookingFor.includes("groom") || lookingFor.includes("male") || lookingFor === "m";
        
        let cardHasFemale = femaleKeywords.some(kw => detailsText.includes(kw)) || detailsText.includes("female");
        let cardHasMale = maleKeywords.some(kw => detailsText.includes(kw)) || detailsText.includes("male");
        
        // If it's ambiguous, we'll give it a pass, but if we clearly know it's a mismatch, we hide it.
        if (isLookingForBride && cardHasMale && !cardHasFemale) {
            matches = false;
        } else if (isLookingForGroom && cardHasFemale && !cardHasMale) {
            matches = false;
        }
      }

      // 2. Age filter
      if (age && (age < ageFrom || age > ageTo)) {
        matches = false;
      }

      // 3. Religion filter
      if (religion && religion !== 'any' && !religion.includes('select')) {
        if (!detailsText.includes(religion)) {
          matches = false;
        }
      }

      // 4. Mother Tongue filter
      if (motherTongue && motherTongue !== 'any' && !motherTongue.includes('select')) {
        if (!detailsText.includes(motherTongue)) {
          matches = false;
        }
      }

      // 5. Location filter
      if (location && location !== 'any' && !location.includes('select')) {
        if (!detailsText.includes(location)) {
          matches = false;
        }
      }

      if (matches) {
        card.style.display = "";
        matchedCount++;
      } else {
        card.style.display = "none";
      }
    });

    // Handle "No Matches Found" DOM injection
    let noMatchMessage = document.getElementById("no-match-msg");
    if (!noMatchMessage) {
      noMatchMessage = document.createElement("div");
      noMatchMessage.id = "no-match-msg";
      noMatchMessage.style.cssText = `
        text-align: center;
        padding: 60px 40px;
        color: #e94057;
        font-family: 'Poppins', sans-serif;
        font-size: 18px;
        font-weight: 600;
        grid-column: 1 / -1;
        width: 100%;
      `;
      noMatchMessage.innerHTML = `
        <i class="fa-solid fa-heart-crack fa-3x mb-3" style="animation: pulse 2s infinite;"></i>
        <br>No matching profiles found.<br>
        <span style="font-size: 13px; font-weight: 400; color: #888;">Try broadening your filters (e.g. selecting Any) or search fields.</span>
      `;
      
      const container = document.querySelector(".profile-container") || document.querySelector(".pm-profile-container") || document.querySelector(".profile-grid-dark");
      if (container) container.appendChild(noMatchMessage);
    }

    if (matchedCount === 0) {
      if (noMatchMessage) noMatchMessage.style.display = "block";
    } else {
      if (noMatchMessage) noMatchMessage.style.display = "none";
    }
  });

  // Handle resets
  const resetBtn = document.querySelector(".pm-reset-btn") || searchForm.querySelector("button[type='reset']");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      // Clear form
      searchForm.reset();
      
      // Display all cards
      const cards = document.querySelectorAll(".profile-container .glass-card, .pm-profile-container .pm-profile-card, .profile-card-dark");
      cards.forEach(card => card.style.display = "");

      const noMatchMessage = document.getElementById("no-match-msg");
      if (noMatchMessage) noMatchMessage.style.display = "none";
    });
  }
});
