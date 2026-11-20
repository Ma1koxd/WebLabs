import os

from infrastructure.database import SessionLocal
from infrastructure.security import hash_password
from infrastructure.sql_book_repository import SqlBookRepository
from infrastructure.sql_user_repository import SqlUserRepository


def main():
    username = os.getenv("SEED_USERNAME", "student")
    password = os.getenv("SEED_PASSWORD", "")
    if len(password) < 8:
        raise RuntimeError("Задайте SEED_PASSWORD длиной не меньше 8 символов в .env")

    with SessionLocal() as session:
        users = SqlUserRepository(session)
        is_first_run = users.get_by_username(username) is None
        if is_first_run:
            users.create(username, hash_password(password))

        books = SqlBookRepository(session)
        # Повторный запуск не дублирует книги и не меняет существующие записи.
        if is_first_run and not books.get_all():
            examples = [
                ("Мастер и Маргарита", "Михаил Булгаков", "Роман о любви и необычных событиях в Москве."),
                ("Преступление и наказание", "Фёдор Достоевский", "История Раскольникова и его раскаяния."),
                ("Маленький принц", "Антуан де Сент-Экзюпери", "Сказка о дружбе и ответственности."),
                ("Капитанская дочка", "Александр Пушкин", "Повесть о чести, любви и верности."),
                ("Ревизор", "Николай Гоголь", "Комедия о чиновниках и неожиданном госте."),
            ]
            for name, author, description in examples:
                books.create(name, author, description)
    print("Тестовые данные готовы.")


if __name__ == "__main__":
    main()
