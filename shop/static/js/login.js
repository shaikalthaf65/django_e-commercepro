
document.addEventListener("DOMContentLoaded", () => {
  let form = document.getElementById("loginForm");
  let backBtn = document.getElementById("backBtn");

  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();

      let email = document.getElementById("email").value.trim();
      let password = document.getElementById("password").value.trim();

      if (email === "" || password === "") {
        alert("Please enter both email and password!");
        return;
      }

      alert("Login Successful ✅");
      window.location.href = "prod.html";
    });
  }
  if (backBtn) {
    backBtn.addEventListener("click", () => {
      window.location.href = "home.html";
    });
  }
});
