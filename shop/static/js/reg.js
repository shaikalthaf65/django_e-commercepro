document.addEventListener("DOMContentLoaded", () => {
  let form = document.getElementById("registerForm");
  let loginBtn = document.getElementById("loginBtn");
  let backBtn = document.getElementById("backBtn");

  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();

      let name = document.getElementById("name").value.trim();
      let email = document.getElementById("email").value.trim();
      let password = document.getElementById("password").value.trim();
      let phone = document.getElementById("phone").value.trim();

      if (!/^[0-9]{10}$/.test(phone)) {
        alert("Please enter a valid 10-digit phone number!");
        return;
      }

      console.log("Registered Details:");
      console.log("Name:", name);
      console.log("Email:", email);
      console.log("Password:", password);
      console.log("Phone:", phone);

      alert("Registration Successful 🎉");
      form.reset();
      window.location.href = "login.html";
    });
  }
  if (loginBtn) {
    loginBtn.addEventListener("click", () => {
      window.location.href = "login.html";
    });
  }
  if (backBtn) {
    backBtn.addEventListener("click", () => {
      window.location.href = "home.html";
    });
  }
});
