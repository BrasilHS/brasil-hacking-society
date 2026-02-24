async function handleFormSubmit(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const url = form.action;

  try {
    const formData = new FormData(form);
    const plainData = Object.fromEntries(formData.entries());
    const jsonData = JSON.stringify(plainData);

    if (!validate_password(plainData)) {
      return
    }

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: jsonData
    });

    if (!response) {
      throw new Error(`Response not received`);
    }

    const result = await response.json();
    const type = Object.keys(result)[0]
    let message = result[type]

    if (Array.isArray(message)) {
      message = message[0]
    }

    showMessage(message, type)

    if (response.status == 201) {
      window.location = "/login"
    }

  } catch (error) {
    console.error("Error sending data:", error);
  }
}

// Attach event listener
document.getElementById("form_register").addEventListener("submit", handleFormSubmit);

const validate_password = (data) => {
  if (data.password.length < 8 ) {
    showMessage("Password minimum length is 8", "error")
    return false
  }

  if (data.password != data.confirm_password) {
    showMessage("Password not match", "error")
    return false
  }

    return true
}
