async function handleFormSubmit(event, redirectMap={}) {
    event.preventDefault();
    const form = event.currentTarget;
    const url = form.action;
    const formData = new FormData(form);
    const plainData = Object.fromEntries(formData.entries());
    const data = JSON.stringify(plainData);

    try {

        const result = await fetch_api(url, data)

        if (redirectMap[result.status]) {
            window.location = redirectMap[result.status]
            const message = result.data?.message
            showMessage(message, "message")
            return
        }

        if (!result.ok) {
            const message = result.data?.error
            showMessage(message, "error")
            return
        }    

    } catch (error) {
        console.error("Error sending data:", error);
    }
}

async function fetch_api(url, data={}, extra_headers={}) {

    const headers = {
        "Content-Type": "application/json",
        ...extra_headers  
    }

    const response = await fetch(url, {
        method: "POST",
        headers: headers,
        body: data
    });

    if (!response) {
        throw new Error(`Response not received`);
    }

    return {
        status: response.status,
        ok: response.ok,
        data: await response.json()
    }
}


function showMessage(message, type = "error") {
    const toast = document.getElementById("toast");
    const span_message = document.getElementById("message");

    span_message.classList.remove("text-red-400", "text-emerald-500");
    span_message.classList.add(type === "error" ? "text-red-400" : "text-emerald-500");
    span_message.textContent = message;

    toast.classList.remove("hidden");
    toast.style.opacity = "1";
}
