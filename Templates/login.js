function showForm(form, event) {
      document.getElementById("login-form").style.display =
        form === "login" ? "block" : "none";

      document.getElementById("register-form").style.display =
        form === "register" ? "block" : "none";

      document.getElementById("logoBox").style.display =
      form === "register" ? "none" : "flex";

      document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
      event.target.classList.add("active");
}