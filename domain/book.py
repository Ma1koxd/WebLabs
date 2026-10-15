from dataclasses import dataclass


@dataclass
class Book:
    """Обычная книга внутри нашей программы."""

    id: int
    name: str
    author: str
    description: str
