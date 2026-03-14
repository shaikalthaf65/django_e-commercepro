document.addEventListener("DOMContentLoaded", () => {
  let registerBtn = document.querySelector("#reg");
  let loginBtn = document.querySelector("#log");

  if (registerBtn) {
    registerBtn.addEventListener("click", () => {
      window.location.href = "reg.html";
    });
  }

  if (loginBtn) {
    loginBtn.addEventListener("click", () => {
      window.location.href = "login.html";
    });
  }
});
