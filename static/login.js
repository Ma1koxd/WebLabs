const form = document.querySelector("#login-form");
const message = document.querySelector("#message");
const submitButton = form.querySelector("button");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    message.textContent = "";
    submitButton.disabled = true;
    try {
        const data = new FormData(form);
        data.set("username", form.elements.username.value.trim());
        const response = await fetch("/api/auth/token", {
            method: "POST",
            body: data,
        });
        if (!response.ok) {
            message.textContent = response.status === 401
                ? "Неверный логин или пароль."
                : await getApiError(response);
            return;
        }
        const result = await response.json();
        sessionStorage.setItem("library_token", result.access_token);
        window.location.href = "/";
    } catch (error) {
        message.textContent = "Не удалось связаться с сервером. Попробуйте ещё раз.";
    } finally {
        submitButton.disabled = false;
    }
});
