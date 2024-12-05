from src.library import Library
from src.messages import MESSAGES


def add_book(library: Library):
    """
    Функция для добавления книги в библиотеку.
    Запрашивает у пользователя данные о книге (название, автор, год),
    выполняет валидацию года и добавляет книгу в библиотеку.
    """
    # Запрашиваем данные
    title = input(MESSAGES["add_prompt_title"])

    author = input(MESSAGES["add_prompt_author"])

    year = input(MESSAGES["add_prompt_year"])

    while True:
        try:
            # Преобразуем введённый год в целое число
            year = int(year)
            break  # Если преобразование прошло успешно, выходим из цикла
        except ValueError:
            # Если возникла ошибка при преобразовании (не число), выводим сообщение об ошибке
            print(MESSAGES["add_year_error"])
            year = input(MESSAGES["add_prompt_year"])  # Просим пользователя ввести год снова

    # Добавляем книгу в библиотеку с полученными данными
    library.add_book(title, author, year)
    # Сообщаем пользователю о том, что книга успешно добавлена
    print(MESSAGES["add_success"])


def delete_book(library: Library):
    """
    Функция для удаления книги из библиотеки по её ID.
    Запрашивает ID книги и, если книга существует, удаляет её.
    """
    while True:
        # Запрашиваем ID книги для удаления
        book_id = input(MESSAGES["delete_prompt_id"])

        try:
            # Преобразуем введённый ID в целое число
            book_id = int(book_id)

            # Пытаемся удалить книгу с заданным ID
            if library.delete_book(book_id=book_id):
                print(MESSAGES["delete_success"])  # Если книга была удалена, сообщаем об этом
                break
            else:
                print(MESSAGES["delete_fail"])  # Если книги с таким ID нет, сообщаем об ошибке
                break
        except ValueError:
            # Если введённое значение не является числом, выводим ошибку
            print(MESSAGES["delete_id_error"])


def search_book(library: Library):
    """
    Функция для поиска книги по названию, автору или году выпуска.
    Запрашивает у пользователя поисковый запрос и выводит результат поиска.
    """
    # Запрашиваем у пользователя критерий поиска (название, автор или год)
    query = input(MESSAGES["search_prompt"])

    # Ищем книгу в библиотеке
    result = library.search_book(query)

    if result:
        # Если книга найдена, выводим её информацию
        print("\n", result)
    else:
        # Если книга не найдена, выводим соответствующее сообщение
        print(MESSAGES["search_not_found"])


def display_books(library: Library):
    """
    Функция для отображения всех книг в библиотеке.
    Если книги есть, выводим их, иначе сообщаем, что книг нет.
    """
    if library.books:
        # Если в библиотеке есть книги, выводим их
        print()
        for book in library.books:
            print("\n", book)  # Выводим информацию о каждой книге
    else:
        # Если книг нет, выводим сообщение
        print(MESSAGES["no_books"])


def change_status(library: Library):
    """
    Функция для изменения статуса книги по её ID.
    Запрашивает ID книги и новый статус, проверяет корректность введённых данных.
    """
    while True:
        # Запрашиваем у пользователя ID книги, статус которой нужно изменить
        book_id = input(MESSAGES["status_prompt_id"])

        try:
            # Преобразуем ID в целое число
            book_id = int(book_id)

            while True:
                # Запрашиваем новый статус книги
                new_status = input(MESSAGES["status_prompt_new"])

                # Проверяем, является ли новый статус допустимым
                if new_status.lower() not in ["в наличии", "выдана"]:
                    print(MESSAGES["status_invalid"])  # Если статус некорректный, выводим ошибку
                else:
                    break  # Если статус корректный, выходим из цикла

            # Пытаемся изменить статус книги
            if library.change_status(book_id=book_id, new_status=new_status):
                print(MESSAGES["status_success"])  # Если статус изменён, сообщаем об этом
                break
            else:
                print(MESSAGES["status_fail"])  # Если книги с таким ID нет, выводим ошибку
                break
        except ValueError:
            # Если ID не является числом, выводим ошибку
            print(MESSAGES["status_id_error"])

