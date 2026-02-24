function showMessage(message, type = "error") {
    const toast = document.getElementById("toast");
    const span_message = document.getElementById("message");

    // remove cores anteriores
    span_message.classList.remove("text-red-400", "text-emerald-500");
    span_message.classList.add(type === "error" ? "text-red-400" : "text-emerald-500");
    span_message.textContent = message;

    // reseta transição
    toast.classList.remove("hidden");
    toast.style.opacity = "1";

}
