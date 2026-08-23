document.addEventListener("DOMContentLoaded", () => {
    // Read the user gender passed from Django backend
    const userGender = window.USER_GENDER ? window.USER_GENDER.toLowerCase() : "";
    
    // If no gender is set (e.g., user not registered), we don't hide anything for now.
    if (!userGender) return;
    
    console.log("Logged-in user gender:", userGender);
    
    // Find all profile cards that have a data-gender attribute
    const cards = document.querySelectorAll('[data-gender]');
    
    cards.forEach(card => {
        const cardGender = card.getAttribute('data-gender').toLowerCase();
        
        // Hide cards that match the user's gender (Male shouldn't see Male)
        if (cardGender === userGender) {
            card.style.display = 'none';
        }
    });
});
