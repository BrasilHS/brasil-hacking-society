// =============================
// GLOBAL EVENT DELEGATION
// =============================

document.addEventListener("submit", function (event) {

    // Reply form
    if (event.target.matches("#reply-form")) {
        handleFormSubmit(event, {
            201: window.location.href,
            302: "/login"
        });
    }

    // Comment form principal
    if (event.target.matches("#form_comment")) {
        handleFormSubmit(event, {
            201: window.location.href,
            302: "/login"
        });
    }

    // Vote forms (exemplo futuro)
    // if (event.target.matches(".vote-form")) {
    //     handleFormSubmit(event);
    // }

    if (event.target.matches("#form_new_post")) {
        handleFormSubmit(event, {
            201: window.location.href,
            302: "/login"
        })
    };

    if (event.target.matches("#form_register")) {
        handleFormSubmit(event, {
            201: "/login"
        })
    }

    if (event.target.matches("#form_login")) {
        handleFormSubmit(event, {
            200: "/"
        })
    };
    
});


// =============================
// GENERIC FORM HANDLER
// =============================

async function handleFormSubmit(event, redirectMap = {}) {

    event.preventDefault();

    const form = event.target; // 🔥 aqui é melhor que currentTarget
    const url = form.action;

    const formData = new FormData(form);
    const plainData = Object.fromEntries(formData.entries());

    for (const key in plainData) {
        if (!plainData[key]) {
            delete plainData[key]
        }
    }

    const data = JSON.stringify(plainData);

    try {

        const result = await fetch_api(url, data);

        if (redirectMap[result.status]) {
            window.location = redirectMap[result.status];
            return;
        }

        if (!result.ok) {
            const message = result.data?.error || "Something went wrong";
            showMessage(message, "error");
            return;
        }

        const message = result.data?.message;
        if (message) {
            showMessage(message, "message");
        }

    } catch (error) {
        console.error("Error sending data:", error);
        showMessage("Network error", "error");
    }
}


// =============================
// FETCH WRAPPER
// =============================

async function fetch_api(url, data = {}, extra_headers = {}) {

    const headers = {
        "Content-Type": "application/json",
        ...extra_headers
    };

    const response = await fetch(url, {
        method: "POST",
        headers: headers,
        body: data
    });

    let response_data = {};

    try {
        response_data = await response.json();
    } catch {
        response_data = {};
    }

    return {
        status: response.status,
        ok: response.ok,
        data: response_data
    };
}


// =============================
// TOAST SYSTEM
// =============================

function showMessage(message, type = "error") {

    const toast = document.getElementById("toast");
    const span_message = document.getElementById("message");

    if (!toast || !span_message) return;

    span_message.classList.remove("text-red-400", "text-emerald-500");
    span_message.classList.add(
        type === "error" ? "text-red-400" : "text-emerald-500"
    );

    span_message.textContent = message;

    toast.classList.remove("hidden");
    toast.style.opacity = "1";

    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.classList.add("hidden"), 300);
    }, 3000);
}
