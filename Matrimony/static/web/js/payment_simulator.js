/* ==========================================================================
   MATRIMONY PORTAL PAYMENT GATEWAY SIMULATION WITH MULTIPLE OPTIONS
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  // Bind buy buttons on pricing cards inside membership.html (if present)
  document.querySelectorAll(".pricing-card").forEach(card => {
    const titleEl = card.querySelector("h3");
    const priceEl = card.querySelector(".price span");
    const buyBtn = card.querySelector("a.btn");

    if (!buyBtn || !titleEl || !priceEl) return;

    const planName = titleEl.innerText.trim();
    const planPrice = priceEl.innerText.trim();

    if (planName.toLowerCase().includes("free")) {
      buyBtn.addEventListener("click", (e) => {
        e.preventDefault();
        alert("🎉 You are now registered on the Free Standard tier!");
      });
      return;
    }

    buyBtn.addEventListener("click", (e) => {
      e.preventDefault();
      window.openPaymentModal(planName, planPrice, () => {
        console.log("Membership page payment success callback triggered.");
      });
    });
  });
});

// Expose openPaymentModal globally on window for registration wizard integration
window.openPaymentModal = (planName, price, successCallback) => {
  let modal = document.getElementById("payment-gateway-modal");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "payment-gateway-modal";
    modal.style.cssText = `
      position: fixed;
      inset: 0;
      z-index: 999999;
      background: rgba(45, 32, 51, 0.65);
      backdrop-filter: blur(8px);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Inter', sans-serif;
    `;
    document.body.appendChild(modal);
  }

  // Render multi-option payment modal structure
  modal.innerHTML = `
    <div class="payment-card" style="
      background: white;
      border-radius: 24px;
      width: 100%;
      max-width: 600px;
      padding: 0;
      box-shadow: 0 25px 50px -12px rgba(233, 64, 87, 0.25);
      border: 1px solid rgba(233, 64, 87, 0.1);
      position: relative;
      overflow: hidden;
      animation: modalFadeIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    ">
      <style>
        @keyframes modalFadeIn {
          from { opacity: 0; transform: scale(0.95) translateY(10px); }
          to { opacity: 1; transform: scale(1) translateY(0); }
        }
        .pay-tab-btn {
          width: 100%;
          text-align: left;
          padding: 15px 20px;
          border: none;
          background: none;
          font-size: 14px;
          font-weight: 600;
          color: #6c757d;
          cursor: pointer;
          border-left: 4px solid transparent;
          transition: all 0.2s;
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .pay-tab-btn.active {
          color: #e94057;
          background: #fff8f9;
          border-left-color: #e94057;
        }
        .pay-tab-btn:hover:not(.active) {
          background: #f8f9fa;
          color: #212529;
        }
        .pay-input::placeholder { color: #ccc; }
        .pay-input:focus {
          border-color: #e94057 !important;
          box-shadow: 0 0 0 3px rgba(233, 64, 87, 0.1) !important;
          outline: none;
        }
        .bank-option {
          border: 1px solid #dee2e6;
          border-radius: 12px;
          padding: 12px;
          text-align: center;
          cursor: pointer;
          transition: all 0.25s;
          font-weight: 500;
          font-size: 13px;
        }
        .bank-option:hover {
          border-color: #e94057;
          background: #fff8f9;
        }
        .bank-option.selected {
          border-color: #e94057;
          background: #fff8f9;
          box-shadow: 0 0 0 3px rgba(233, 64, 87, 0.1);
        }
        .wallet-option {
          display: flex;
          align-items: center;
          justify-content: space-between;
          border: 1px solid #dee2e6;
          border-radius: 12px;
          padding: 15px 20px;
          margin-bottom: 12px;
          cursor: pointer;
          transition: all 0.2s;
        }
        .wallet-option:hover, .wallet-option.selected {
          border-color: #e94057;
          background: #fff8f9;
        }
      </style>

      <!-- Top Brand Header Bar -->
      <div style="background: linear-gradient(135deg, #e94057 0%, #fd5e53 100%); padding: 20px; color: white; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <h4 style="margin: 0; font-weight: 700; display: flex; align-items: center; gap: 8px; font-family: 'Poppins', sans-serif;">
            <i class="fa-solid fa-shield-halved"></i> Razorpay Secure Checkout
          </h4>
          <span style="font-size: 11px; opacity: 0.85;">Transaction: TXN_${Math.floor(Math.random()*900000+100000)} | Plan: ${planName}</span>
        </div>
        <button id="close-payment-btn" style="background: none; border: none; font-size: 22px; color: white; cursor: pointer; padding: 5px;">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <!-- Main Columns -->
      <div style="display: flex; min-height: 380px;">
        <!-- Left Tab Navigation Sidebar -->
        <div style="width: 35%; border-right: 1px solid #f0f0f0; background: #fafafa; padding-top: 15px;">
          <button class="pay-tab-btn active" data-tab="card-tab">
            <i class="fa-solid fa-credit-card"></i> Card Details
          </button>
          <button class="pay-tab-btn" data-tab="qr-tab">
            <i class="fa-solid fa-qrcode"></i> UPI QR Scanner
          </button>
          <button class="pay-tab-btn" data-tab="net-tab">
            <i class="fa-solid fa-building-columns"></i> Net Banking
          </button>
          <button class="pay-tab-btn" data-tab="wallet-tab">
            <i class="fa-solid fa-wallet"></i> Wallets (Paytm)
          </button>

          <div style="padding: 30px 20px 20px; text-align: center; border-top: 1px solid #eee; margin-top: 40px;">
            <span style="font-size: 11px; color: #8a7f8c; display: block; font-weight: 500;">Payable Amount</span>
            <strong style="color: #2d2033; font-size: 20px; font-weight: 800;">${price}</strong>
          </div>
        </div>

        <!-- Right Side Tab Contents -->
        <div id="tab-contents-pane" style="width: 65%; padding: 25px; position: relative;">
          <!-- 1. CARD TAB (Default) -->
          <div id="card-tab" class="tab-pane" style="display: block;">
            <form class="pay-form-engine" id="payment-simulator-form" data-type="Card">
              <h5 style="font-weight: 700; color: #2d2033; margin-bottom: 18px; font-size: 15px;">Enter Credit/Debit Card</h5>

              <div style="margin-bottom: 12px;">
                <label style="display: block; font-size: 11px; font-weight: 600; color: #555; margin-bottom: 4px;">Cardholder Name</label>
                <input type="text" class="pay-input" placeholder="e.g. Omkar Patil" required style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 10px; font-size: 13px; box-sizing: border-box; transition: all 0.25s;" />
              </div>

              <div style="margin-bottom: 12px;">
                <label style="display: block; font-size: 11px; font-weight: 600; color: #555; margin-bottom: 4px;">Card Number</label>
                <div style="position: relative;">
                  <input type="text" id="payCardNo" class="pay-input" placeholder="4111 2222 3333 4444" pattern="\\d{4}\\s?\\d{4}\\s?\\d{4}\\s?\\d{4}" maxlength="19" required style="width: 100%; padding: 8px 12px 8px 36px; border: 1px solid #ddd; border-radius: 10px; font-size: 13px; box-sizing: border-box; transition: all 0.25s;" />
                  <i class="fa-solid fa-credit-card" style="position: absolute; left: 12px; top: 11px; color: #aaa; font-size: 13px;"></i>
                </div>
              </div>

              <div style="display: flex; gap: 12px; margin-bottom: 20px;">
                <div style="flex: 1;">
                  <label style="display: block; font-size: 11px; font-weight: 600; color: #555; margin-bottom: 4px;">Expiry Date</label>
                  <input type="text" placeholder="MM/YY" pattern="(0[1-9]|1[0-2])\\/?([2-9][0-9])" maxlength="5" required class="pay-input" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 10px; font-size: 13px; box-sizing: border-box; transition: all 0.25s;" />
                </div>
                <div style="flex: 1;">
                  <label style="display: block; font-size: 11px; font-weight: 600; color: #555; margin-bottom: 4px;">CVV</label>
                  <input type="password" placeholder="***" pattern="\\d{3}" maxlength="3" required class="pay-input" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 10px; font-size: 13px; box-sizing: border-box; transition: all 0.25s;" />
                </div>
              </div>

              <button type="submit" class="btn-pay-action" style="width: 100%; padding: 12px; border-radius: 12px; background: #e94057; border: none; color: white; font-weight: 700; font-size: 14px; cursor: pointer; box-shadow: 0 6px 15px rgba(233, 64, 87, 0.2); transition: all 0.3s;">
                Pay ${price} via Card
              </button>
            </form>
          </div>

          <!-- 2. UPI / QR SCANNER TAB -->
          <div id="qr-tab" class="tab-pane" style="display: none; text-align: center;">
            <h5 style="font-weight: 700; color: #2d2033; margin-bottom: 12px; font-size: 15px; text-align: left;">Scan QR Code to Pay</h5>

            <div style="background: white; border: 1px solid #eee; border-radius: 16px; padding: 12px; width: 170px; height: 170px; margin: 0 auto 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
              <!-- Render a beautiful SVG QR Code placeholder -->
              <svg width="140" height="140" viewBox="0 0 100 100" style="color: #2d2033;">
                <rect x="0" y="0" width="25" height="25" fill="currentColor"/>
                <rect x="5" y="5" width="15" height="15" fill="white"/>
                <rect x="8" y="8" width="9" height="9" fill="currentColor"/>

                <rect x="75" y="0" width="25" height="25" fill="currentColor"/>
                <rect x="80" y="5" width="15" height="15" fill="white"/>
                <rect x="83" y="8" width="9" height="9" fill="currentColor"/>

                <rect x="0" y="75" width="25" height="25" fill="currentColor"/>
                <rect x="5" y="80" width="15" height="15" fill="white"/>
                <rect x="8" y="83" width="9" height="9" fill="currentColor"/>

                <!-- Random noise blocks for QR likeness -->
                <rect x="35" y="5" width="10" height="5" fill="currentColor"/>
                <rect x="35" y="15" width="5" height="10" fill="currentColor"/>
                <rect x="50" y="0" width="10" height="15" fill="currentColor"/>
                <rect x="50" y="20" width="15" height="5" fill="currentColor"/>
                <rect x="65" y="10" width="5" height="15" fill="currentColor"/>
                <rect x="80" y="35" width="10" height="10" fill="currentColor"/>
                <rect x="90" y="50" width="5" height="15" fill="currentColor"/>
                <rect x="15" y="35" width="10" height="5" fill="currentColor"/>
                <rect x="5" y="50" width="5" height="15" fill="currentColor"/>
                <rect x="35" y="45" width="30" height="30" fill="currentColor"/>
                <rect x="45" y="55" width="10" height="10" fill="white"/>
                <rect x="75" y="75" width="10" height="5" fill="currentColor"/>
                <rect x="85" y="85" width="15" height="5" fill="currentColor"/>
                <rect x="90" y="70" width="5" height="10" fill="currentColor"/>
              </svg>
            </div>

            <p class="text-muted" style="font-size: 11px; margin-bottom: 12px; line-height: 1.4;">
              Scan this QR using any UPI app (GPay, PhonePe, Paytm, BHIM) to complete transaction securely.
            </p>

            <button id="simulate-qr-success-btn" style="width: 100%; padding: 12px; border-radius: 12px; background: #e94057; border: none; color: white; font-weight: 700; font-size: 14px; cursor: pointer; box-shadow: 0 6px 15px rgba(233, 64, 87, 0.2); transition: all 0.3s;">
              <i class="fa-solid fa-spinner fa-spin-pulse me-2" id="qr-loading-spinner" style="display: none;"></i>
              Simulate QR Scan Success
            </button>
          </div>

          <!-- 3. NET BANKING TAB -->
          <div id="net-tab" class="tab-pane" style="display: none;">
            <h5 style="font-weight: 700; color: #2d2033; margin-bottom: 15px; font-size: 15px;">Popular Indian Banks</h5>

            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 25px;">
              <div class="bank-option selected" data-bank="SBI"><i class="fa-solid fa-building-columns text-primary me-2"></i> SBI</div>
              <div class="bank-option" data-bank="HDFC"><i class="fa-solid fa-building-columns text-info me-2"></i> HDFC</div>
              <div class="bank-option" data-bank="ICICI"><i class="fa-solid fa-building-columns text-warning me-2"></i> ICICI</div>
              <div class="bank-option" data-bank="Axis"><i class="fa-solid fa-building-columns text-danger me-2"></i> Axis</div>
            </div>

            <button id="netbank-pay-btn" style="width: 100%; padding: 12px; border-radius: 12px; background: #e94057; border: none; color: white; font-weight: 700; font-size: 14px; cursor: pointer; box-shadow: 0 6px 15px rgba(233, 64, 87, 0.2); transition: all 0.3s;">
              Pay ${price} via SBI Netbanking
            </button>
          </div>

          <!-- 4. WALLETS TAB -->
          <div id="wallet-tab" class="tab-pane" style="display: none;">
            <h5 style="font-weight: 700; color: #2d2033; margin-bottom: 15px; font-size: 15px;">Select Wallet</h5>

            <div class="wallet-option selected" data-wallet="Paytm">
              <span style="font-weight: 600; color: #002970;"><i class="fa-solid fa-wallet me-2 text-primary"></i> Paytm Wallet</span>
              <i class="fa-regular fa-circle-dot" style="color: #e94057;"></i>
            </div>

            <div class="wallet-option" data-wallet="PhonePe">
              <span style="font-weight: 600; color: #5f259f;"><i class="fa-solid fa-wallet me-2 text-secondary"></i> PhonePe Wallet</span>
              <i class="fa-regular fa-circle" style="color: #ccc;"></i>
            </div>

            <button id="wallet-pay-btn" style="width: 100%; padding: 12px; border-radius: 12px; background: #e94057; border: none; color: white; font-weight: 700; font-size: 14px; cursor: pointer; box-shadow: 0 6px 15px rgba(233, 64, 87, 0.2); transition: all 0.3s; margin-top: 15px;">
              Pay ${price} via Paytm Wallet
            </button>
          </div>
        </div>
      </div>
    </div>
  `;

  modal.style.display = "flex";

  // Close btn listener
  document.getElementById("close-payment-btn").addEventListener("click", () => {
    modal.style.display = "none";
  });

  // Formatting Card Number with spaces
  const cardInput = document.getElementById("payCardNo");
  if(cardInput) {
    cardInput.addEventListener("input", function(e) {
      let val = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
      let formatted = '';
      for (let i = 0; i < val.length; i++) {
        if (i > 0 && i % 4 === 0) formatted += ' ';
        formatted += val[i];
      }
      e.target.value = formatted;
    });
  }

  // Handle Tab Switch Actions
  const tabButtons = modal.querySelectorAll(".pay-tab-btn");
  const tabPanes = modal.querySelectorAll(".tab-pane");

  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      // Toggle Active Tab Btn
      tabButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      // Toggle Display Pane
      const targetTab = btn.getAttribute("data-tab");
      tabPanes.forEach(pane => {
        if (pane.id === targetTab) {
          pane.style.display = "block";
        } else {
          pane.style.display = "none";
        }
      });
    });
  });

  // Handle Netbanking selection
  const bankOptions = modal.querySelectorAll(".bank-option");
  const netbankPayBtn = document.getElementById("netbank-pay-btn");
  bankOptions.forEach(opt => {
    opt.addEventListener("click", () => {
      bankOptions.forEach(o => o.classList.remove("selected"));
      opt.classList.add("selected");
      const bank = opt.getAttribute("data-bank");
      if (netbankPayBtn) netbankPayBtn.innerText = `Pay ${price} via ${bank} Netbanking`;
    });
  });

  // Handle Wallet selection
  const walletOptions = modal.querySelectorAll(".wallet-option");
  const walletPayBtn = document.getElementById("wallet-pay-btn");
  walletOptions.forEach(opt => {
    opt.addEventListener("click", () => {
      walletOptions.forEach(o => {
        o.classList.remove("selected");
        o.querySelector("i").className = "fa-regular fa-circle";
        o.querySelector("i").style.color = "#ccc";
      });
      opt.classList.add("selected");
      opt.querySelector("i").className = "fa-regular fa-circle-dot";
      opt.querySelector("i").style.color = "#e94057";

      const wallet = opt.getAttribute("data-wallet");
      if (walletPayBtn) walletPayBtn.innerText = `Pay ${price} via ${wallet} Wallet`;
    });
  });

  // --- TRIGGER SUCCESS SCREEN HELPER ---
  const triggerSuccessState = () => {
    const payCard = modal.querySelector(".payment-card");
    if(payCard) {
      payCard.innerHTML = `
        <div style="text-align: center; padding: 50px 30px; font-family: 'Inter', sans-serif;">
          <div style="
            width: 80px;
            height: 80px;
            background: #f4fff8;
            border: 2px solid #1fa55b;
            color: #1fa55b;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            margin-bottom: 24px;
            animation: scaleSuccess 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
          ">
            <style>
              @keyframes scaleSuccess {
                from { transform: scale(0.5); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
              }
            </style>
            <i class="fa-solid fa-check"></i>
          </div>
          <h3 style="font-weight: 700; color: #1fa55b; margin-bottom: 12px; font-family: 'Poppins', sans-serif;">Payment Successful!</h3>
          <p style="font-size: 14px; color: #555; line-height: 1.6; margin-bottom: 30px; max-width: 380px; margin-inline: auto;">
            Thank you! Your purchase of <strong>${planName}</strong> is complete. Your subscription is upgraded instantly.
          </p>
        <a href="/profiles/search/basic/" style="text-decoration: none;">
  <button id="success-ok-btn" style="
    padding: 12px 40px;
    border-radius: 25px;
    background: #1fa55b;
    color: white;
    font-weight: 700;
    font-size: 14px;
    border: none;
    cursor: pointer;
    box-shadow: 0 6px 15px rgba(31, 165, 91, 0.2);
    transition: all 0.25s;
  ">
    Awesome!
  </button>
</a>
        </div>
      `;

      // Close modal on click and trigger successCallback
      document.getElementById("success-ok-btn").addEventListener("click", () => {
        modal.style.display = "none";

        // Update payment flags in localStorage
        localStorage.setItem("isPaid", "true");
        localStorage.setItem("selectedPlan", planName);

        let currentUser = null;
        try {
          currentUser = JSON.parse(localStorage.getItem("currentUser"));
        } catch(e) {}

        if (currentUser) {
          currentUser.isPaid = "true";
          currentUser.planName = planName;
          localStorage.setItem("currentUser", JSON.stringify(currentUser));

          let registeredUsers = [];
          try {
            registeredUsers = JSON.parse(localStorage.getItem("registeredUsers")) || [];
          } catch(e) {}

          const idx = registeredUsers.findIndex(u => u.email === currentUser.email || u.mobile === currentUser.mobile);
          if (idx !== -1) {
            registeredUsers[idx].isPaid = "true";
            registeredUsers[idx].planName = planName;
            localStorage.setItem("registeredUsers", JSON.stringify(registeredUsers));
          }
        }

        if (successCallback) successCallback();

        // Redirect to basic search page after successful payment
        window.location.href = "/profiles/search/basic/";
      });
    }
  };

  // --- MOCK PAYMENT TRIGGERS ---

  // A. Card submit handler
  document.getElementById("payment-simulator-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const btn = modal.querySelector(".btn-pay-action");
    if(btn) {
      btn.disabled = true;
      btn.style.opacity = "0.8";
      btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin me-2"></i> Processing card payment...`;
    }
    setTimeout(() => {
      triggerSuccessState();
    }, 2000);
  });

  // B. QR code click trigger
  document.getElementById("simulate-qr-success-btn").addEventListener("click", () => {
    const btn = document.getElementById("simulate-qr-success-btn");
    const spinner = document.getElementById("qr-loading-spinner");
    if (btn && spinner) {
      spinner.style.display = "inline-block";
      btn.disabled = true;
      btn.style.opacity = "0.8";
    }
    setTimeout(() => {
      triggerSuccessState();
    }, 2000);
  });

  // C. Netbanking click trigger
  if (netbankPayBtn) {
    netbankPayBtn.addEventListener("click", () => {
      netbankPayBtn.disabled = true;
      netbankPayBtn.style.opacity = "0.8";
      netbankPayBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin me-2"></i> Connecting bank server...`;
      setTimeout(() => {
        triggerSuccessState();
      }, 2000);
    });
  }

  // D. Wallet click trigger
  if (walletPayBtn) {
    walletPayBtn.addEventListener("click", () => {
      walletPayBtn.disabled = true;
      walletPayBtn.style.opacity = "0.8";
      walletPayBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin me-2"></i> Accessing wallet...`;
      setTimeout(() => {
        triggerSuccessState();
      }, 2000);
    });
  }
};
