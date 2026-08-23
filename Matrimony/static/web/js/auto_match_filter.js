/* ==========================================================================
   AUTO MATCH FILTER (auto_match_filter.js)
   Automatically filters dummy cards on Match pages based on saved profile preferences
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    // Check if we are on a matches page
    const isMatchPage = window.location.pathname.includes("match");
    if (!isMatchPage) return;
  
    // Get preferences from localStorage
    // Attempt to load from JSON object first, fallback to individual items
    let profileData = {};
    try {
        const stored = localStorage.getItem("currentUserProfile");
        if (stored) {
            profileData = JSON.parse(stored);
        }
    } catch (e) {
        console.error("Could not parse profile data", e);
    }
    
    // Read values, defaulting to separate keys if JSON is missing, else defaults
    const prefAgeMin = parseInt(profileData.prefAgeMin || localStorage.getItem('prefAgeMin')) || 18;
    const prefAgeMax = parseInt(profileData.prefAgeMax || localStorage.getItem('prefAgeMax')) || 100;
    const prefReligion = (profileData.prefReligion || localStorage.getItem('prefReligion') || "").toLowerCase().trim();
    const prefMotherTongue = (profileData.prefMotherTongue || localStorage.getItem('prefMotherTongue') || "").toLowerCase().trim();
    const prefLocation = (profileData.prefLocation || localStorage.getItem('prefLocation') || "").toLowerCase().trim();
    const prefGender = (profileData.gender || localStorage.getItem('prefGender') || "").toLowerCase().trim(); // If user is Male, they seek Female (handled in logic or save)
    const prefCaste = (profileData.prefCaste || localStorage.getItem('prefCaste') || "").toLowerCase().trim();
    
    // Simple heuristic lists for dummy data filtering
    const femaleKeywords = ["snehal", "priya", "riya", "anjali", "neha", "pooja", "shreya", "aarti", "kavita", "swati", "nisha", "ehadiyen"];
    const maleKeywords = ["rahul", "rohit", "amit", "vikas", "sachin", "manish", "sunil", "anil", "vijay", "sanjay", "ajay"];
  
    const cards = document.querySelectorAll(".profile-container .glass-card, .pm-profile-container .pm-profile-card, .profile-card-dark");
    let matchedCount = 0;
  
    cards.forEach(card => {
        const detailsText = card.textContent.toLowerCase();
        
        // Extract Age from card
        const ageMatch = detailsText.match(/age:\s*(\d+)/i) || detailsText.match(/\b(\d+)\s*•/);
        const age = ageMatch ? parseInt(ageMatch[1]) : null;
  
        let matches = true;
  
        // 1. Gender Filter (If profile is Male, looking for Female)
        if (prefGender && prefGender !== "any") {
          let isLookingForBride = prefGender === "male"; // if user is male, he seeks bride
          let isLookingForGroom = prefGender === "female"; // if user is female, she seeks groom
          
          let cardHasFemale = femaleKeywords.some(kw => detailsText.includes(kw)) || detailsText.includes("female");
          let cardHasMale = maleKeywords.some(kw => detailsText.includes(kw)) || detailsText.includes("male");
          
          if (isLookingForBride && cardHasMale && !cardHasFemale) {
              matches = false;
          } else if (isLookingForGroom && cardHasFemale && !cardHasMale) {
              matches = false;
          }
        }
  
        // 2. Age filter
        if (age && (age < prefAgeMin || age > prefAgeMax)) {
          matches = false;
        }
  
        // 3. Religion filter
        if (prefReligion && prefReligion !== 'any') {
          if (!detailsText.includes(prefReligion)) {
            matches = false;
          }
        }
  
        // 4. Mother Tongue filter
        if (prefMotherTongue && prefMotherTongue !== 'any') {
          if (!detailsText.includes(prefMotherTongue)) {
            matches = false;
          }
        }
  
        // 5. Location filter
        if (prefLocation && prefLocation !== 'any') {
          if (!detailsText.includes(prefLocation)) {
            matches = false;
          }
        }

        // 6. Caste filter
        if (prefCaste && prefCaste !== 'any') {
          if (!detailsText.includes(prefCaste)) {
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
  
    // Handle "No Matches Found" UI
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
          <br>No profiles match your saved preferences.<br>
          <span style="font-size: 13px; font-weight: 400; color: #888;">Go to your Profile settings to broaden your preferences.</span>
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
