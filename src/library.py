import json

from src.book import Book

import os

# Получение пути к файлу относительно текущей директории



# Теперь используйте file_path для открытия или записи в файл

class Library:
    """
    Класс для управления библиотекой книг.
    Предоставляет функции для добавления, удаления, поиска книг, а также изменения их статуса.
    """

    def __init__(self, data_file: str = 'books.json'):
        """
        Инициализирует объект библиотеки.
        :param data_file: Путь к файлу, где хранятся данные о книгах.
        """
        self.data_file = data_file  # Путь к файлу с данными о книгах
        self.books = self.load_books()  # Загрузка книг из файла
        self.next_id = self.get_next_id()  # Определяем следующий доступный ID для книги

    def get_next_id(self) -> int:
        """
        Определяет следующий доступный уникальный ID для новой книги.
        Если библиотека пуста, возвращается 1.
        :return: Следующий уникальный ID.
        """
        if not self.books:
            return 1
        # Ищем максимальный ID среди всех книг и увеличиваем на 1
        max_id = max(book.book_id for book in self.books) + 1
        return max_id

    def load_books(self) -> list[Book]:
        """
        Загружает книги из файла JSON в список объектов Book.
        Если файл не найден, создаёт файл и возвращает пустой список.
        :return: Список объектов Book.
        """
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                # Чтение JSON данных и создание объектов Book
                books = [Book(**book) for book in json.load(file)]
                return books
        except FileNotFoundError:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump([], file)
            # Если файл не найден, создаём файл и возвращаем пустой список
            return []

    def save_books(self):
        """
        Сохраняет список книг в файл JSON.
        Каждая книга преобразуется в словарь с помощью __dict__.
        """
        with open(self.data_file, 'w', encoding='utf-8') as file:
            # Сохраняем данные книг в формате JSON
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """
        Добавляет новую книгу в библиотеку.
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        """
        # Создаём объект книги с уникальным ID
        book = Book(book_id=self.next_id, title=title, author=author, year=year)
        self.books.append(book)  # Добавляем книгу в список
        self.next_id += 1  # Увеличиваем ID для следующей книги
        self.save_books()  # Сохраняем изменения в файл

    def delete_book(self, book_id: int) -> bool:
        """
        Удаляет книгу из библиотеки по ID.
        :param book_id: ID книги, которую нужно удалить.
        :return: True, если книга была найдена и удалена, иначе False.
        """
        for book in self.books:
            if book.book_id == book_id:
                self.books.remove(book)  # Удаляем книгу
                self.save_books()  # Сохраняем изменения
                return True
        # Если книга с таким ID не найдена, возвращаем False
        return False

    def search_book(self, query: str) -> Book | None:
        """
        Ищет книгу в библиотеке по названию, автору или году.
        :param query: Поисковый запрос (может быть названием, автором или годом).
        :return: Найденная книга или None, если книга не найдена.
        """
        for book in self.books:
            # Сравниваем запрос с полями книги (название, автор, год)
            if query.lower() == book.title.lower():
                return book
            elif query.lower() == book.author.lower():
                return book
            elif query == str(book.year):
                return book
        # Если книга не найдена, возвращаем None
        return None

    def change_status(self, book_id: int, new_status: str) -> bool:
        """
        Изменяет статус книги по ID.
        :param book_id: ID книги, статус которой нужно изменить.
        :param new_status: Новый статус книги.
        :return: True, если статус был изменён, иначе False.
        """
        for book in self.books:
            if book.book_id == book_id:
                book.status = new_status  # Изменяем статус книги
                self.save_books()  # Сохраняем изменения в файл
                return True
        # Если книга с таким ID не найдена, возвращаем False
        return False
