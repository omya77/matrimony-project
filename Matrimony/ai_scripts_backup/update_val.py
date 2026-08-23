import re

with open("Template/web/personal.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Mobile
html = re.sub(r'id="userMobile"(.*?)maxlength="15" pattern="\^\\\\\+\?\[0-9\\\\s\\\\-\]\{10,15\}\\\$"\s*/?>', r'id="userMobile"\1maxlength="10" minlength="10" pattern="^[0-9]{10}$"/>', html)

# 2. Update text inputs
html = re.sub(r'(id="(userFullName|userMotherTongue|userCaste|highestEducation|university|state|city|prefMotherTongue|prefEducation|prefLocation)"[^>]*?)maxlength="(\d+)"', r'\1maxlength="\3" minlength="3" pattern="^[a-zA-Z \.,]+$"', html)

# 3. JS Replacement
old_js = """          const requiredInputs = activePage.querySelectorAll("[required]");
          let isValid = true;

          requiredInputs.forEach((input) => {
            // Find or create invalid-feedback div
            let feedback = input.parentNode.querySelector(".invalid-feedback");
            if (!feedback) {
              feedback = document.createElement("div");
              feedback.className = "invalid-feedback";
              feedback.style.display = "none";
              feedback.innerHTML = `<i class="fa-solid fa-circle-exclamation me-1"></i> This field is required.`;
              input.parentNode.appendChild(feedback);
            }

            if (
              !input.value.trim() ||
              (input.type === "checkbox" && !input.checked) ||
              (input.tagName === "SELECT" && (!input.value || input.value.startsWith("Select")))
            ) {
              isValid = false;
              input.classList.remove("is-valid");
              input.classList.add("is-invalid");
              feedback.style.display = "block";

              // Listen to input to clear validation error
              const clearError = () => {
                input.classList.remove("is-invalid");
                feedback.style.display = "none";
                if(input.value.trim() && !(input.tagName === "SELECT" && input.value.startsWith("Select"))) {
                  input.classList.add("is-valid");
                }
              };

              input.addEventListener("input", clearError, { once: true });
              input.addEventListener("change", clearError, { once: true });
            } else {
              input.classList.remove("is-invalid");
              input.classList.add("is-valid");
              feedback.style.display = "none";
            }
          });"""

new_js = """          const requiredInputs = activePage.querySelectorAll("[required], input[pattern]");
          let isValid = true;

          requiredInputs.forEach((input) => {
            // Find or create invalid-feedback div
            let feedback = input.parentNode.querySelector(".invalid-feedback");
            if (!feedback) {
              feedback = document.createElement("div");
              feedback.className = "invalid-feedback";
              feedback.style.display = "none";
              input.parentNode.appendChild(feedback);
            }

            let fieldIsValid = true;
            let errorMessage = "This field is required.";

            if (input.tagName === "SELECT" && (!input.value || input.value.startsWith("Select"))) {
              fieldIsValid = false;
              errorMessage = "Please select a valid option.";
            } else if (input.type === "checkbox" && !input.checked) {
              fieldIsValid = false;
              errorMessage = "You must check this box.";
            } else if (input.value && !input.checkValidity()) {
              fieldIsValid = false;
              if (input.validity.patternMismatch) {
                if (input.type === "tel") errorMessage = "Enter a valid 10-digit mobile number.";
                else errorMessage = "Only letters/spaces are allowed (no numbers/special chars).";
              } else if (input.validity.tooShort) {
                errorMessage = `Minimum length is ${input.minLength} characters.`;
              } else if (input.validity.rangeUnderflow || input.validity.rangeOverflow) {
                errorMessage = `Value must be between ${input.min} and ${input.max}.`;
              } else if (input.validity.typeMismatch) {
                if (input.type === "email") errorMessage = "Enter a valid email address.";
                else errorMessage = "Invalid format.";
              }
            } else if (!input.value.trim() && input.required) {
               fieldIsValid = false;
            }

            if (!fieldIsValid) {
              isValid = false;
              input.classList.remove("is-valid");
              input.classList.add("is-invalid");
              feedback.innerHTML = `<i class="fa-solid fa-circle-exclamation me-1"></i> ${errorMessage}`;
              feedback.style.display = "block";

              const clearError = () => {
                input.classList.remove("is-invalid");
                feedback.style.display = "none";
                if(input.value.trim() && !(input.tagName === "SELECT" && input.value.startsWith("Select")) && input.checkValidity()) {
                  input.classList.add("is-valid");
                }
              };
              input.addEventListener("input", clearError, { once: true });
              input.addEventListener("change", clearError, { once: true });
            } else {
              input.classList.remove("is-invalid");
              if (input.value.trim() && !(input.tagName === "SELECT" && input.value.startsWith("Select"))) {
                  input.classList.add("is-valid");
              }
              feedback.style.display = "none";
            }
          });"""

if old_js in html:
    html = html.replace(old_js, new_js)
    print("JS Block updated successfully.")
else:
    print("Could not find JS Block!")

with open("Template/web/personal.html", "w", encoding="utf-8") as f:
    f.write(html)
