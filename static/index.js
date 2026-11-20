const bookList = document.querySelector("#book-list");
const bookCount = document.querySelector("#book-count");
const message = document.querySelector("#message");
const authStatus = document.querySelector("#auth-status");
const loginLink = document.querySelector("#login-link");
const logoutButton = document.querySelector("#logout-button");
const addLink = document.querySelector("#add-link");
let currentUser = null;

function updateAuthControls() {
    loginLink.hidden = currentUser !== null;
    logoutButton.hidden = currentUser === null;
    addLink.hidden = currentUser === null;
    authStatus.textContent = currentUser
        ? `Вы вошли как ${currentUser.username}`
        : "Вы просматриваете библиотеку без входа.";
}

logoutButton.addEventListener("click", () => {
    sessionStorage.removeItem("library_token");
    window.location.reload();
});

async function loadBooks() {
    try {
        const response = await apiFetch("/api/books");
        if (!response.ok) {
            message.textContent = await getApiError(response);
            return;
        }
        const books = await response.json();
        bookCount.textContent = `${books.length} из 50`;
        bookList.innerHTML = "";
        if (books.length === 0) {
            bookList.innerHTML = '<p class="empty">Книг пока нет.</p>';
            return;
        }
        for (const book of books) {
            const card = document.createElement("article");
            card.className = "book-card";
            const info = document.createElement("a");
            info.className = "book-info";
            info.href = `/details.html?id=${book.id}`;
            const name = document.createElement("h3");
            name.textContent = book.name;
            const author = document.createElement("p");
            author.textContent = book.author;
            info.append(name, author);
            card.append(info);

            if (currentUser) {
                const deleteButton = document.createElement("button");
                deleteButton.className = "small-delete";
                deleteButton.textContent = "Удалить";
                deleteButton.addEventListener("click", () => deleteBook(book.id));
                card.append(deleteButton);
            }
            bookList.append(card);
        }
    } catch (error) {
        message.textContent = "Не удалось получить список книг. Проверьте соединение с сервером.";
    }
}

async function deleteBook(bookId) {
    if (!currentUser || !sessionStorage.getItem("library_token")) {
        message.textContent = "Нужно войти в аккаунт, чтобы удалить книгу.";
        return;
    }
    if (!confirm("Удалить эту книгу?")) {
        return;
    }
    message.textContent = "";
    try {
        const response = await apiFetch(`/api/books/${bookId}`, { method: "DELETE" });
        if (!response.ok) {
            message.textContent = await getApiError(response);
            if (response.status === 401) {
                currentUser = null;
                updateAuthControls();
                await loadBooks();
            }
            return;
        }
        await loadBooks();
    } catch (error) {
        message.textContent = "Не удалось связаться с сервером. Попробуйте ещё раз.";
    }
}

async function startPage() {
    try {
        currentUser = await getCurrentUser();
    } catch (error) {
        message.textContent = "Не удалось проверить вход. Попробуйте обновить страницу.";
    }
    updateAuthControls();
    await loadBooks();
}

startPage();
