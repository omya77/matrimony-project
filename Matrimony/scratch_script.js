
      // ==========================================
      // SCRIPT.JS PART 1
      // AGE CALCULATION
      // PASSWORD TOGGLE
      // PASSWORD STRENGTH
      // CONFIRM PASSWORD CHECK
      // ==========================================

      // ===============================
      // AOS INITIALIZE
      // ===============================

      AOS.init({
        once: true,
        duration: 800,
      });

      // ===============================
      // AGE CALCULATION
      // ===============================

      function calculateAge() {
        const dob = document.getElementById("dobInput").value;

        if (!dob) {
          return;
        }

        const birthDate = new Date(dob);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();

        if (
          monthDiff < 0 ||
          (monthDiff === 0 && today.getDate() < birthDate.getDate())
        ) {
          age--;
        }

        const ageInput = document.getElementById("ageInput");

        if (age >= 21) {
          ageInput.value = age + " Years";
          ageInput.classList.add("valid");
          ageInput.classList.remove("invalid");
        } else {
          ageInput.value = "Min. Age 21";
          ageInput.classList.add("invalid");
          ageInput.classList.remove("valid");
          document.getElementById("dobInput").value = "";
        }
      }

      // ===============================
      // PASSWORD SHOW / HIDE
      // ===============================

      function togglePassword(inputId, icon) {
        const input = document.getElementById(inputId);

        if (input.type === "password") {
          input.type = "text";

          icon.classList.remove("fa-eye");

          icon.classList.add("fa-eye-slash");
        } else {
          input.type = "password";

          icon.classList.remove("fa-eye-slash");

          icon.classList.add("fa-eye");
        }
      }

      // ===============================
      // PASSWORD STRENGTH
      // ===============================

      function checkStrength() {
        const password = document.getElementById("passwordInput").value;

        const bars = document.querySelectorAll(".strength-meter span");

        const label = document.getElementById("strengthLabel");

        let score = 0;

        if (password.length >= 6) {
          score++;
        }

        if (password.length >= 10) {
          score++;
        }

        if (/[A-Z]/.test(password) && /[0-9]/.test(password)) {
          score++;
        }

        if (/[^A-Za-z0-9]/.test(password)) {
          score++;
        }

        const text = ["Weak", "Fair", "Good", "Strong"];

        bars.forEach((bar, index) => {
          if (index < score) {
            bar.style.background =
              score === 1
                ? "#e94057"
                : score === 2
                  ? "#ff9800"
                  : score === 3
                    ? "#ffd700"
                    : "#18b368";
          } else {
            bar.style.background = "#ececec";
          }
        });

        label.innerText =
          password.length > 0
            ? "Password Strength : " + text[Math.max(score - 1, 0)]
            : "Password strength";
      }

      // ===============================
      // CONFIRM PASSWORD CHECK
      // ===============================

      function checkPasswordMatch() {
        const password = document.getElementById("passwordInput").value;

        const confirm = document.getElementById("confirmPassword").value;

        const message = document.getElementById("passwordMessage");

        if (confirm.length === 0) {
          message.innerHTML = "";
          return;
        }

        if (password === confirm) {
          message.innerHTML = "✔ Password matched";

          message.className = "password-match success";
        } else {
          message.innerHTML = "✖ Password not matched";

          message.className = "password-match error";
        }
      }

      // ==========================================
      // SCRIPT.JS PART 2
      // MOBILE VERIFY
      // EMAIL VERIFY
      // GOVERNMENT ID VERIFY
      // OTP MODAL CONTROL
      // ==========================================

      let currentVerifyType = "";

      let verifiedStatus = {
        mobile: false,

        email: false,

        government: false,
      };

      // ===============================
      // OPEN OTP MODAL
      // ===============================

        let timerInterval;
        function startResendTimer() {
            clearInterval(timerInterval);
            let timeLeft = 30;
            document.getElementById("resendTimerText").style.display = "inline";
            document.getElementById("resendBtn").style.display = "none";
            document.getElementById("timerValue").innerText = timeLeft;
            
            timerInterval = setInterval(() => {
                timeLeft--;
                document.getElementById("timerValue").innerText = timeLeft;
                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    document.getElementById("resendTimerText").style.display = "none";
                    document.getElementById("resendBtn").style.display = "inline";
                }
            }, 1000);
        }

        function resendOTP() {
            startResendTimer();
            if (currentVerifyType === "mobile") {
                const mobile = document.getElementById("mobileInput").value.trim();
                fetch('/accounts/api/send_mobile_otp/', {
                  credentials: 'same-origin',
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ mobile: mobile })
                }).then(res => res.json()).then(data => { if(data.status !== 'success') alert(data.message); });
            } else if (currentVerifyType === "email") {
                const email = document.getElementById("emailInput").value.trim();
                fetch('/accounts/api/send_otp/', {
                  credentials: 'same-origin',
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ email: email })
                }).then(res => res.json()).then(data => { if(data.status !== 'success') alert(data.message); });
            } else if (currentVerifyType === "government") {
                const id = document.getElementById("idInput").value.trim();
                const mobile = document.getElementById("mobileInput").value.trim();
                fetch('/accounts/api/send_id_otp/', {
                  credentials: 'same-origin',
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ id: id, mobile: mobile })
                }).then(res => res.json()).then(data => { if(data.status !== 'success') alert(data.message); });
            }
        }

      function openOTPModal(type) {
        currentVerifyType = type;
        startResendTimer();

        document.getElementById("otpModal").style.display = "flex";

        document.querySelectorAll(".otp-field").forEach((input) => {
          input.value = "";
        });

        document.getElementById("otp1").focus();

        const otpText = document.getElementById("otpText");

        if (type === "mobile") {
          otpText.innerHTML = "Enter OTP sent to your mobile number.";
        } else if (type === "email") {
          otpText.innerHTML = "Enter OTP sent to your email address.";
        } else {
          otpText.innerHTML = "Enter OTP sent for Government ID verification.";
        }
      }

      // ===============================
      // MOBILE VERIFY
      // ===============================

      function verifyMobile() {
        const mobileField = document.getElementById("mobileInput");
        const mobile = mobileField.value.trim();
        
        const mobilePattern = /^[6-9]\d{9}$/;
        if (!mobilePattern.test(mobile)) {
          alert("Please enter valid 10 digit mobile number.");
          return;
        }

        // Keep 10 digits strict
        mobileField.value = mobile;


        document.getElementById("mobileVerifyBtn").innerHTML = "Sending...";
        fetch('/accounts/api/send_mobile_otp/', {
          credentials: 'same-origin',
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ mobile: mobile })
        })
        .then(res => res.json())
        .then(data => {
          document.getElementById("mobileVerifyBtn").innerHTML = "Verify";
          if (data.status === 'success') {
            openOTPModal("mobile");
          } else {
            alert(data.message);
          }
        }).catch(err => {
          document.getElementById("mobileVerifyBtn").innerHTML = "Verify";
          console.error(err);
        });
      }

      // ===============================
      // EMAIL VERIFY
      // ===============================

      function verifyEmail() {
        const email = document.getElementById("emailInput").value.trim();
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
          alert("Please enter valid email address.");
          return;
        }
        
        // Backend Integration: Send OTP
        document.getElementById("emailVerifyBtn").innerHTML = "Sending...";
        fetch('/accounts/api/send_otp/', {
          credentials: 'same-origin',
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email })
        })
        .then(res => res.json())
        .then(data => {
          document.getElementById("emailVerifyBtn").innerHTML = "Verify";
          if (data.status === 'success') {
            openOTPModal("email");
          } else {
            alert(data.message);
          }
        }).catch(err => {
          document.getElementById("emailVerifyBtn").innerHTML = "Verify";
          console.error(err);
        });
      }

      // ===============================
      // GOVERNMENT ID VERIFY
      // ===============================

      function updateIdPlaceholder() {
          const type = document.getElementById("idType").value;
          const input = document.getElementById("idInput");
          input.value = "";
          if (type === "Aadhaar") {
              input.placeholder = "Enter Aadhaar Number (12 digits)";
              input.maxLength = 12;
          } else {
              input.placeholder = "Enter PAN Number (10 alphanumeric)";
              input.maxLength = 10;
          }
      }

      function verifyGovernmentID() {
        const type = document.getElementById("idType").value;
        const id = document.getElementById("idInput").value.trim();
        
        if (type === "Aadhaar") {
            const idPattern = /^\d{12}$/;
            if (!idPattern.test(id)) {
                alert("Please enter valid 12 digit Aadhaar number.");
                return;
            }
        } else if (type === "PAN") {
            const panPattern = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/i;
            if (!panPattern.test(id)) {
                alert("Please enter valid 10 character PAN number.");
                return;
            }
        }

        const mobileForId = document.getElementById("mobileInput").value.trim();
        if (!mobileForId || mobileForId.length !== 10) {
            alert("Please verify your mobile number first.");
            return;
        }
        document.getElementById("idVerifyBtn").innerHTML = "Sending...";
        fetch('/accounts/api/send_id_otp/', {
          credentials: 'same-origin',
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: id, mobile: mobileForId })
        })
        .then(res => res.json())
        .then(data => {
          document.getElementById("idVerifyBtn").innerHTML = "Verify";
          if (data.status === 'success') {
            openOTPModal("government");
          } else {
            alert(data.message);
          }
        }).catch(err => {
          document.getElementById("idVerifyBtn").innerHTML = "Verify";
          console.error(err);
        });
      }

      // ===============================
      // OTP NEXT INPUT
      // ===============================

      function moveNext(current, nextId) {
        if (current.value.length >= 1) {
          document.getElementById(nextId).focus();
        }
      }

      // ===============================
      // OTP VERIFY
      // ===============================

      function verifyOTP() {
        let otp = "";
        document.querySelectorAll(".otp-field").forEach((input) => {
          otp += input.value;
        });

        const btn = document.getElementById("verifyOtpSubmitBtn");
        if(btn.disabled) return;
        btn.disabled = true;
        btn.innerHTML = "Verifying... <i class='fa-solid fa-spinner fa-spin'></i>";

        if (currentVerifyType === "email") {
          fetch('/accounts/api/verify_otp/', {
          credentials: 'same-origin',
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ otp: otp })
          })
          .then(res => res.json())
          .then(data => {
            btn.disabled = false;
            btn.innerHTML = "Submit & Verify <i class='fa-solid fa-check'></i>";
            if (data.status === 'success') {
              document.getElementById("otpModal").style.display = "none";
              verifiedStatus[currentVerifyType] = true;
              updateVerifyButton(currentVerifyType);
              alert("Verification completed successfully.");
            } else {
              alert("Invalid OTP. Please enter correct OTP.");
            }
          }).catch(err => {
              btn.disabled = false;
              btn.innerHTML = "Submit & Verify <i class='fa-solid fa-check'></i>";
          });
        } else if (currentVerifyType === "mobile") {
          fetch('/accounts/api/verify_mobile_otp/', {
          credentials: 'same-origin',
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ otp: otp })
          })
          .then(res => res.json())
          .then(data => {
            btn.disabled = false;
            btn.innerHTML = "Submit & Verify <i class='fa-solid fa-check'></i>";
            if (data.status === 'success') {
              document.getElementById("otpModal").style.display = "none";
              verifiedStatus[currentVerifyType] = true;
              updateVerifyButton(currentVerifyType);
              alert("Verification completed successfully.");
            } else {
              alert("Invalid OTP. Please enter correct OTP.");
            }
          }).catch(err => {
              btn.disabled = false;
              btn.innerHTML = "Submit & Verify <i class='fa-solid fa-check'></i>";
          });
        } else if (currentVerifyType === "government") {
          fetch('/accounts/api/verify_id_otp/', {
          credentials: 'same-origin',
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ otp: otp })
          })
          .then(res => res.json())
          .then(data => {
            btn.disabled = false;
            btn.innerHTML = "Submit & Verify <i class='fa-solid fa-check'></i>";
            if (data.status === 'success') {
              document.getElementById("otpModal").style.display = "none";
              verifiedStatus[currentVerifyType] = true;
              updateVerifyButton(currentVerifyType);
              alert("Verification completed successfully.");
            } else {
              alert("Invalid OTP. Please enter correct OTP.");
            }
          }).catch(err => {
              btn.disabled = false;
              btn.innerHTML = "Submit & Verify <i class='fa-solid fa-check'></i>";
          });
        }
      }

      // ===============================
      // UPDATE VERIFY BUTTON
      // ===============================

      function updateVerifyButton(type) {
        let button;

        if (type === "mobile") {
          button = document.getElementById("mobileVerifyBtn");
        } else if (type === "email") {
          button = document.getElementById("emailVerifyBtn");
        } else {
          button = document.getElementById("idVerifyBtn");
        }

        button.classList.add("is-verified");

        button.innerHTML = '<i class="fa-solid fa-check"></i> Verified';
      }

      // ==========================================
      // SCRIPT.JS PART 3
      // REGISTER VALIDATION
      // FINAL SUBMIT CHECK
      // CLOSE MODAL
      // ==========================================

      // ===============================
      // REGISTER SUBMIT
      // ===============================

      function handleRegister(event) {
        event.preventDefault();

        const firstName = document.getElementById("firstName").value.trim();

        const lastName = document.getElementById("lastName").value.trim();

        const gender = document.getElementById("gender").value;

        const dob = document.getElementById("dobInput").value;

        const password = document.getElementById("passwordInput").value;

        const confirmPassword =
          document.getElementById("confirmPassword").value;

        const consent = document.getElementById("consentCheck").checked;

        // ===============================
        // BASIC VALIDATION
        // ===============================

        if (
          firstName === "" ||
          lastName === "" ||
          gender === "" ||
          dob === ""
        ) {
          alert("Please complete all required fields.");

          return;
        }

        // ===============================
        // AGE CHECK
        // ===============================

        const ageText = document.getElementById("ageInput").value;

        if (ageText.includes("Minimum")) {
          alert("Age must be 18 or above.");

          return;
        }

        // ===============================
        // PASSWORD CHECK
        // ===============================

        if (password.length < 6) {
          alert("Password must contain minimum 6 characters.");

          return;
        }

        if (password !== confirmPassword) {
          alert("Password and confirm password do not match.");

          return;
        }

        // ===============================
        // VERIFICATION CHECK
        // ===============================

        if (!verifiedStatus.mobile) {
          alert("Please verify your mobile number first.");

          return;
        }

        if (!verifiedStatus.email) {
          alert("Please verify your email first.");

          return;
        }

        if (!verifiedStatus.government) {
          alert("Please verify your Government ID first.");

          return;
        }

        // ===============================
        // TERMS CHECK
        // ===============================

        if (!consent) {
          alert("Please accept Terms and Privacy Policy.");

          return;
        }

        // ===============================
        // SUCCESS
        // ===============================

        const email = document.getElementById("emailInput").value.trim();
        const mobile = document.getElementById("mobileInput").value.trim();

        const newUser = {
          firstName: firstName,
          lastName: lastName,
          email: email,
          mobile: mobile,
          gender: gender,
          dob: dob,
          password: password,
          isPaid: "false",
          planName: ""
        };

        let registeredUsers = [];
        try {
          registeredUsers = JSON.parse(localStorage.getItem("registeredUsers")) || [];
        } catch(err) {
          registeredUsers = [];
        }

        // Backend Integration: Create User
        fetch('/accounts/api/create_user/', {
          credentials: 'same-origin',
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newUser)
        })
        .then(res => res.json())
        .then(data => {
          if (data.status === 'success') {
            // Keep localStorage logic so frontend state remains intact
            const exists = registeredUsers.some(u => u.email === email || u.mobile === mobile);
            if (!exists) {
              registeredUsers.push(newUser);
              localStorage.setItem("registeredUsers", JSON.stringify(registeredUsers));
            }
            localStorage.setItem("currentUser", JSON.stringify(newUser));
            localStorage.setItem("isLoggedIn", "true");
            localStorage.setItem("isPaid", "false");

            alert("🎉 Registration Completed Successfully! Redirecting you to complete your profile...");
            window.location.href = "/profiles/personal/";
          } else {
            alert(data.message);
          }
        }).catch(err => {
          console.error(err);
        });
      }

      // ===============================
      // CLOSE OTP WHEN CLICK OUTSIDE
      // ===============================

      document
        .getElementById("otpModal")
        .addEventListener("click", function (e) {
          if (e.target === this) {
            this.style.display = "none";
          }
        });

      // ===============================
      // ONLY NUMBERS FOR OTP
      // ===============================

      const otpInputs = document.querySelectorAll(".otp-field");
      otpInputs.forEach((input, index) => {
        input.addEventListener("input", function () {
          this.value = this.value.replace(/[^0-9]/g, "");
        });
        
        input.addEventListener("keydown", function (e) {
          if (e.key === "Backspace" && this.value === "") {
            if (index > 0) {
              otpInputs[index - 1].focus();
            }
          }
        });
      });
      // ===============================
      // CLOSE OTP MODAL BUTTON
      // ===============================

      function closeOTPModal() {
        document.getElementById("otpModal").style.display = "none";
      }
    