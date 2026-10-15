const bookList = document.querySelector("#book-list");
const bookCount = document.querySelector("#book-count");
const message = document.querySelector("#message");

async function loadBooks() {
    try {
        const response = await fetch("/api/books");
        const books = await response.json();

        bookCount.textContent = `${books.length} из 50`;
        bookList.innerHTML = "";

        if (books.length === 0) {
            bookList.innerHTML = '<p class="empty">Книг пока нет. Добавьте первую книгу.</p>';
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

            const deleteButton = document.createElement("button");
            deleteButton.className = "small-delete";
            deleteButton.textContent = "Удалить";
            deleteButton.addEventListener("click", () => deleteBook(book.id));

            card.append(info, deleteButton);
            bookList.append(card);
        }
    } catch (error) {
        message.textContent = "Не удалось получить список книг.";
    }
}

async function deleteBook(bookId) {
    if (!confirm("Удалить эту книгу?")) {
        return;
    }

    const response = await fetch(`/api/books/${bookId}`, { method: "DELETE" });
    if (response.ok) {
        loadBooks();
    } else {
        message.textContent = "Не удалось удалить книгу.";
    }
}

loadBooks();
