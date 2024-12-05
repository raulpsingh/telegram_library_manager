
class Book:
    """
    Класс, представляющий книгу в библиотеке.
    Содержит информацию о книге: ID, название, автор, год издания и статус.
    """

    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "В наличии"):
        """
        Инициализирует объект книги с указанными параметрами.

        :param book_id: Уникальный идентификатор книги.
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :param status: Статус книги, по умолчанию "В наличии".
        """
        self.book_id = book_id  # Уникальный идентификатор книги
        self.title = title      # Название книги
        self.author = author    # Автор книги
        self.year = year        # Год издания
        self.status = status    # Статус книги, может быть "В наличии" или "Выдана"

    def __repr__(self) -> str:
        """
        Переопределяет метод __repr__, чтобы выводить строковое представление объекта.

        """
        # Возвращаем строку, представляющую книгу в удобном для чтения формате
        return f"{self.book_id}. {self.title} - {self.author} ({self.year}) - {self.status}"
