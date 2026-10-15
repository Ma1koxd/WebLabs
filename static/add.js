const form = document.querySelector("#book-form");
const message = document.querySelector("#message");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    message.textContent = "";

    const book = {
        name: form.name.value.trim(),
        author: form.author.value.trim(),
        description: form.description.value.trim(),
    };

    const response = await fetch("/api/books", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(book),
    });

    if (response.ok) {
        const createdBook = await response.json();
        window.location.href = `/details.html?id=${createdBook.id}`;
        return;
    }

    const error = await response.json();
    message.textContent = error.detail || "Не удалось добавить книгу.";
});
