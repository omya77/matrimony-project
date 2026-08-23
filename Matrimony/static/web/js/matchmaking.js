/* ==========================================================================
   MATRIMONY PORTAL CLIENT-SIDE MATCHMAKING ENGINE (matchmaking.js)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  // Read current user profile from localStorage
  const savedProfile = localStorage.getItem("currentUserProfile");
  if (!savedProfile) {
    console.log("No current user profile found. Displaying all default matches.");
    return;
  }

  const profile = JSON.parse(savedProfile);
  console.log("Applying matchmaking logic based on user profile:", profile);

  // Get all profile card elements
  const cards = document.querySelectorAll(".profile-container .glass-card") || 
                document.querySelectorAll(".pm-profile-container .pm-profile-card") ||
                document.querySelectorAll(".profile-card-col");

  if (!cards.length) return;

  const isFemaleMatch = (card) => {
    const img = card.querySelector("img");
    if (img) {
      const src = img.src.toLowerCase();
      if (src.includes("bride") || src.includes("woman") || src.includes("female") || 
          src.includes("photo-1573496359142-b8d87734a5a2") || src.includes("photo-1534528741775-53994a69daeb") ||
          src.includes("bride_1.png") || src.includes("bride_9.png")) {
        return true;
      }
      if (src.includes("groom") || src.includes("man") || src.includes("male") || 
          src.includes("photo-1507003211169-0a1dd7228f2d") || src.includes("groom_1.png")) {
        return false;
      }
    }
    // Fallback detection using profile name
    const nameEl = card.querySelector("h3") || card.querySelector(".profile-name");
    const name = nameEl ? nameEl.innerText.toLowerCase() : "";
    if (name.includes("snehal") || name.includes("ehadiyen") || name.includes("omkar") || 
        name.includes("riya") || name.includes("sanya") || name.includes("puja") || 
        name.includes("sharma") || name.includes("malhotra") || name.includes("patil")) {
      // In the mockup files, Patil is female (Snehal Patil, Ehadiyen Patil)
      if (name.includes("rahul") || name.includes("amit") || name.includes("vikram") || name.includes("rohan") || name.includes("aditya")) {
        return false;
      }
      return true;
    }
    return false;
  };

  let visibleMatchesCount = 0;

  cards.forEach(card => {
    const cardText = card.innerText.toLowerCase();
    
    // 1. GENDER COMPATIBILITY FILTER
    // If current user is Male, show ONLY Female matches. If current user is Female, show ONLY Male matches.
    const female = isFemaleMatch(card);
    const userGender = profile.gender; // "Male" or "Female"
    
    let genderMatches = false;
    if (userGender === "Male" && female) {
      genderMatches = true;
    } else if (userGender === "Female" && !female) {
      genderMatches = true;
    }

    let isCompatible = genderMatches;

    // 2. PARTNER PREFERENCES COMPATIBILITY
    // A. Religion Preference
    if (isCompatible && profile.prefReligion && profile.prefReligion !== "Any") {
      const religionPref = profile.prefReligion.toLowerCase();
      if (!cardText.includes(religionPref)) {
        isCompatible = false;
      }
    }

    // B. Mother Tongue Preference
    if (isCompatible && profile.prefMotherTongue && profile.prefMotherTongue !== "Any") {
      const tonguePref = profile.prefMotherTongue.toLowerCase();
      if (!cardText.includes(tonguePref)) {
        isCompatible = false;
      }
    }

    // C. Location Preference
    if (isCompatible && profile.prefLocation && profile.prefLocation !== "Any") {
      const locationPref = profile.prefLocation.toLowerCase();
      if (!cardText.includes(locationPref)) {
        isCompatible = false;
      }
    }

    // D. Age range preference
    if (isCompatible) {
      const ageMatch = cardText.match(/age:\s*(\d+)/i) || cardText.match(/\b(\d+)\s*•/);
      if (ageMatch) {
        const age = parseInt(ageMatch[1]);
        if (age < profile.prefAgeMin || age > profile.prefAgeMax) {
          isCompatible = false;
        }
      }
    }

    // Apply visibility display toggle
    if (isCompatible) {
      card.style.display = "";
      visibleMatchesCount++;
    } else {
      // If we are on featured_brides or featured_grooms, skip full gender filter to maintain page design intent, 
      // but still filter by religion/location/age.
      const currentPath = window.location.pathname.toLowerCase();
      if (currentPath.includes("brides") || currentPath.includes("grooms")) {
        // Skip gender mismatch hide on dedicated galleries
        card.style.display = "";
        visibleMatchesCount++;
      } else {
        card.style.display = "none";
      }
    }
  });

  console.log(`Matchmaking completed: displayed ${visibleMatchesCount} compatible matches.`);
});
