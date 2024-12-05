import unittest
from src.library import Library
from src.book import Book


class TestLibraryMethods(unittest.TestCase):
    """
    Тесты для класса Library.
    """

    def setUp(self):
        """
        Метод setup, который выполняется перед каждым тестом.
        Создаём тестовую библиотеку с несколькими книгами.
        """
        self.library = Library(data_file="test_books.json")
        self.library.books = [
            Book(book_id=1, title="Изучаем Python", author="Эрик Мэтиз", year=2024, status="В наличии"),
            Book(book_id=2, title="Грокаем Алгоритмы", author="Адитья Бхаргава", year=2017, status="Выдана")
        ]
        self.library.next_id = 3  # Устанавливаем следующий ID для добавления новых книг

    def test_add_book(self):
        """Тест добавления книги."""
        self.library.add_book("A Byte of Python", "Swaroop Chitlur", 2023)
        # Проверяем, что книга была добавлена
        self.assertEqual(len(self.library.books), 3)
        self.assertEqual(self.library.books[2].title, "A Byte of Python")
        self.assertEqual(self.library.books[2].author, "Swaroop Chitlur")

    def test_delete_book(self):
        """Тест удаления книги по ID."""
        # Удаляем книгу с ID 1
        result = self.library.delete_book(1)
        self.assertTrue(result)  # Книга должна быть удалена
        self.assertEqual(len(self.library.books), 1)  # Должно остаться 1 книга
        # Проверяем, что книга с ID 1 была удалена
        self.assertEqual(self.library.books[0].title, "Грокаем Алгоритмы")

    def test_delete_non_existent_book(self):
        """Тест попытки удаления несуществующей книги."""
        result = self.library.delete_book(999)  # Книги с таким ID нет
        self.assertFalse(result)  # Ожидаем, что книга не была удалена

    def test_search_book_by_title(self):
        """Тест поиска книги по названию."""
        result = self.library.search_book("Изучаем Python")
        self.assertIsNotNone(result)
        self.assertEqual(result.title, "Изучаем Python")

    def test_search_book_by_author(self):
        """Тест поиска книги по автору."""
        result = self.library.search_book("Адитья Бхаргава")
        self.assertIsNotNone(result)
        self.assertEqual(result.author, "Адитья Бхаргава")

    def test_search_book_by_year(self):
        """Тест поиска книги по году."""
        result = self.library.search_book("2024")
        self.assertIsNotNone(result)
        self.assertEqual(result.year, 2024)

    def test_search_book_not_found(self):
        """Тест поиска книги, которая не существует."""
        result = self.library.search_book("Такой книги нет")
        self.assertIsNone(result)  # Ожидаем, что книга не найдена

    def test_change_status(self):
        """Тест изменения статуса книги."""
        # Изменяем статус книги с ID 2
        result = self.library.change_status(2, "В наличии")
        self.assertTrue(result)  # Статус должен быть изменён
        self.assertEqual(self.library.books[0].status, "В наличии")

    def test_change_status_invalid_id(self):
        """Тест изменения статуса книги с несуществующим ID."""
        result = self.library.change_status(999, "Выдана")
        self.assertFalse(result)  # Ожидаем, что статус не изменится




if __name__ == "__main__":
    unittest.main()
