const form = document.querySelector("#book-form");
const message = document.querySelector("#message");
const loginHint = document.querySelector("#login-hint");
const submitButton = form.querySelector("button");
let currentUser = null;

async function checkLogin() {
    try {
        currentUser = await getCurrentUser();
        form.hidden = currentUser === null;
        loginHint.hidden = currentUser !== null;
    } catch (error) {
        message.textContent = "Не удалось проверить вход. Попробуйте обновить страницу.";
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!currentUser || !sessionStorage.getItem("library_token")) {
        message.textContent = "Нужно войти в аккаунт, чтобы добавить книгу.";
        return;
    }
    message.textContent = "";
    submitButton.disabled = true;
    try {
        const book = {
            name: form.elements["name"].value.trim(),
            author: form.elements.author.value.trim(),
            description: form.elements.description.value.trim(),
        };
        const response = await apiFetch("/api/books", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(book),
        });
        if (!response.ok) {
            message.textContent = await getApiError(response);
            if (response.status === 401) {
                currentUser = null;
                form.hidden = true;
                loginHint.hidden = false;
            }
            return;
        }
        const createdBook = await response.json();
        window.location.href = `/details.html?id=${createdBook.id}`;
    } catch (error) {
        message.textContent = "Не удалось связаться с сервером. Попробуйте ещё раз.";
    } finally {
        submitButton.disabled = false;
    }
});

checkLogin();
