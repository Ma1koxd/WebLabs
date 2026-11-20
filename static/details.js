const form = document.querySelector("#book-form");
const pageTitle = document.querySelector("#page-title");
const message = document.querySelector("#message");
const deleteButton = document.querySelector("#delete-button");
const bookActions = document.querySelector("#book-actions");
const loginHint = document.querySelector("#login-hint");
const saveButton = form.querySelector('button[type="submit"]');
const bookId = new URLSearchParams(window.location.search).get("id");
let currentUser = null;

function updateEditing() {
    const canEdit = currentUser !== null;
    form.elements["name"].readOnly = !canEdit;
    form.elements.author.readOnly = !canEdit;
    form.elements.description.readOnly = !canEdit;
    bookActions.hidden = !canEdit;
    loginHint.hidden = canEdit;
}

async function loadBook() {
    if (!bookId) {
        pageTitle.textContent = "Не указан номер книги";
        return;
    }
    try {
        const response = await apiFetch(`/api/books/${bookId}`);
        if (!response.ok) {
            pageTitle.textContent = "Не удалось открыть книгу";
            message.textContent = await getApiError(response);
            return;
        }
        const book = await response.json();
        pageTitle.textContent = book.name;
        form.elements["name"].value = book.name;
        form.elements.author.value = book.author;
        form.elements.description.value = book.description;
        form.hidden = false;
        updateEditing();
    } catch (error) {
        pageTitle.textContent = "Не удалось открыть книгу";
        message.textContent = "Не удалось связаться с сервером. Попробуйте ещё раз.";
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!currentUser || !sessionStorage.getItem("library_token")) {
        message.textContent = "Нужно войти в аккаунт, чтобы изменить книгу.";
        return;
    }
    message.textContent = "";
    saveButton.disabled = true;
    try {
        const book = {
            name: form.elements["name"].value.trim(),
            author: form.elements.author.value.trim(),
            description: form.elements.description.value.trim(),
        };
        const response = await apiFetch(`/api/books/${bookId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(book),
        });
        if (!response.ok) {
            message.textContent = await getApiError(response);
            if (response.status === 401) {
                currentUser = null;
                updateEditing();
            }
            return;
        }
        const updatedBook = await response.json();
        pageTitle.textContent = updatedBook.name;
        message.textContent = "Изменения сохранены.";
    } catch (error) {
        message.textContent = "Не удалось связаться с сервером. Попробуйте ещё раз.";
    } finally {
        saveButton.disabled = false;
    }
});

deleteButton.addEventListener("click", async () => {
    if (!currentUser || !sessionStorage.getItem("library_token")) {
        message.textContent = "Нужно войти в аккаунт, чтобы удалить книгу.";
        return;
    }
    if (!confirm("Удалить эту книгу?")) {
        return;
    }
    message.textContent = "";
    deleteButton.disabled = true;
    try {
        const response = await apiFetch(`/api/books/${bookId}`, { method: "DELETE" });
        if (!response.ok) {
            message.textContent = await getApiError(response);
            if (response.status === 401) {
                currentUser = null;
                updateEditing();
            }
            return;
        }
        window.location.href = "/";
    } catch (error) {
        message.textContent = "Не удалось связаться с сервером. Попробуйте ещё раз.";
    } finally {
        deleteButton.disabled = false;
    }
});

async function startPage() {
    try {
        currentUser = await getCurrentUser();
    } catch (error) {
        message.textContent = "Не удалось проверить вход. Попробуйте обновить страницу.";
    }
    await loadBook();
}

startPage();
