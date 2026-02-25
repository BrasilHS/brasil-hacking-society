// Attach event listener
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form_login")

  if (form) {
    form.addEventListener("submit", (e) => {
      handleFormSubmit(e)
    });
  }
})


