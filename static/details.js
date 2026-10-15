const form = document.querySelector("#book-form");
const pageTitle = document.querySelector("#page-title");
const message = document.querySelector("#message");
const deleteButton = document.querySelector("#delete-button");
const bookId = new URLSearchParams(window.location.search).get("id");

async function loadBook() {
    if (!bookId) {
        pageTitle.textContent = "Не указан номер книги";
        return;
    }

    const response = await fetch(`/api/books/${bookId}`);
    if (!response.ok) {
        pageTitle.textContent = "Книга не найдена";
        return;
    }

    const book = await response.json();
    pageTitle.textContent = book.name;
    form.name.value = book.name;
    form.author.value = book.author;
    form.description.value = book.description;
    form.hidden = false;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    message.textContent = "";

    const book = {
        name: form.name.value.trim(),
        author: form.author.value.trim(),
        description: form.description.value.trim(),
    };

    const response = await fetch(`/api/books/${bookId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(book),
    });

    if (response.ok) {
        const updatedBook = await response.json();
        pageTitle.textContent = updatedBook.name;
        message.textContent = "Изменения сохранены.";
    } else {
        message.textContent = "Не удалось сохранить изменения.";
    }
});

deleteButton.addEventListener("click", async () => {
    if (!confirm("Удалить эту книгу?")) {
        return;
    }

    const response = await fetch(`/api/books/${bookId}`, { method: "DELETE" });
    if (response.ok) {
        window.location.href = "/";
    } else {
        message.textContent = "Не удалось удалить книгу.";
    }
});

loadBook();
