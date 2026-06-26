const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwqHF7KahVwGIDiSQSIX_6VPQVg5syk-BYu-y3xdVyKguZnJmvSxKlk7ZqWvRIgnm88/exec";
const form = document.getElementById("contactForm");
const submitBtn = form.querySelector('button[type="submit"]');
const formMessage = document.createElement("div");
formMessage.classList.add("form-message");
form.appendChild(formMessage);

function showError(message) {
  formMessage.textContent = message;
  formMessage.className = "form-message error";
}

function showSuccess(message) {
  formMessage.textContent = message;
  formMessage.className = "form-message success";
}

form.addEventListener("submit", function (e) {
  e.preventDefault();

  submitBtn.disabled = true;

  const formData = new FormData(form);

  fetch(SCRIPT_URL, {
    method: "POST",
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        showSuccess("Your message has been sent.");
        form.reset();
        if (window.turnstile) turnstile.reset();
      } else {
        showError(data.error || "Submission failed.");
      }
      submitBtn.disabled = false;
    })
    .catch(() => {
      showError("Network error. Please try again.");
    });
});
