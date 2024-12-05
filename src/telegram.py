import os
import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from src import keyboards
from src.library import Library
from src.messages import MESSAGES
from src.states import CurrentStates
from dotenv import load_dotenv

# Получите ваш API токен, который вы получили у BotFather

# Настройка переменных для работы с состояниями
author, title, year = str(), str(), int()  # Переменные для хранения данных книги
book_id_change = int()  # Переменная для хранения ID книги, статус которой изменяется

# Инициализация бота и диспетчера
  # Создание диспетчера для обработки сообщений
router = Router()  # Создание маршрутизатора для управления маршрутами

# Создаём экземпляр библиотеки
library = Library()  # Экземпляр библиотеки для работы с книгами


# Команда /start с кнопками
@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    """
    Обработчик команды /start.
    Устанавливает начальное состояние и отправляет меню с кнопками.
    """
    await state.set_state(CurrentStates.waiting_for_click)  # Устанавливаем состояние ожидания действия
    await message.answer("Hello", reply_markup=keyboards.keyboard())  # Отправляем меню


# Обработчик для кнопки "Добавить книгу"
@router.message(F.text == 'Добавить книгу')
async def add_book_button(message: types.Message, state: FSMContext):
    """
    Обработчик для кнопки "Добавить книгу".
    Переводит в состояние ожидания ввода названия книги.
    """
    await state.set_state(CurrentStates.waiting_for_book_title)  # Состояние: ожидание названия книги
    await message.answer(MESSAGES["add_prompt_title"])  # Запрос на ввод названия книги


@router.message(F.text == 'Изменить статус')
async def add_book_button(message: types.Message, state: FSMContext):
    """
    Обработчик для кнопки "Изменить статус".
    Переводит в состояние ожидания ID книги.
    """
    await state.set_state(CurrentStates.waiting_for_id_to_change)  # Состояние: ожидание ID книги
    await message.answer(MESSAGES["status_prompt_id"])  # Запрос на ввод ID книги


# Обработчик для кнопки "Удалить книгу"
@router.message(F.text == "Удалить книгу")
async def delete_book_button(message: types.Message, state: FSMContext):
    """
    Обработчик для кнопки "Удалить книгу".
    Переводит в состояние ожидания ID книги для удаления.
    """
    await state.set_state(CurrentStates.waiting_for_id_to_delete)  # Состояние: ожидание ID книги
    await message.answer(MESSAGES["delete_prompt_id"])  # Запрос на ввод ID книги


# Обработчик для кнопки "Найти книгу"
@router.message(F.text == 'Найти книгу')
async def search_book_button(message: types.Message, state: FSMContext):
    """
    Обработчик для кнопки "Найти книгу".
    Переводит в состояние ожидания поискового запроса.
    """
    await state.set_state(CurrentStates.waiting_for_query)  # Состояние: ожидание поискового запроса
    await message.answer(MESSAGES["search_prompt"])  # Запрос на ввод поискового запроса


# Обработчик для кнопки "Показать все книги"
@router.message(F.text == 'Показать все книги')
async def display_books_button(message: types.Message):
    """
    Обработчик для кнопки "Показать все книги".
    Отображает все книги, если они есть.
    """
    if library.books:
        for book in library.books:
            await message.answer(str(book))  # Отправляем информацию о каждой книге
    else:
        await message.answer(MESSAGES["no_books"])  # Сообщаем, что книг нет


@router.message(F.text)
async def add_book(message: types.Message, state: FSMContext):
    """
    Универсальный обработчик для различных состояний:
    - Добавление книги
    - Удаление книги
    - Изменение статуса
    - Поиск книги
    """
    global year, title, author, book_id_change
    current_state = await state.get_state()  # Получаем текущее состояние FSM

    # Добавление книги
    if current_state == CurrentStates.waiting_for_book_title:
        title = message.text  # Сохраняем название книги
        await state.set_state(CurrentStates.waiting_for_book_author)  # Состояние: ожидание автора книги
        await message.answer(MESSAGES["add_prompt_author"])  # Запрос на ввод автора книги

    elif current_state == CurrentStates.waiting_for_book_author:
        author = message.text  # Сохраняем автора книги
        await state.set_state(CurrentStates.waiting_for_book_year)  # Состояние: ожидание года выпуска
        await message.answer(MESSAGES["add_prompt_year"])  # Запрос на ввод года выпуска

    elif current_state == CurrentStates.waiting_for_book_year:
        if message.text.isnumeric():  # Проверяем, что введённый год — число
            year = message.text  # Сохраняем год выпуска
            await state.set_state(CurrentStates.waiting_for_click)  # Возвращаем в состояние ожидания действий
        else:
            await message.answer(MESSAGES["add_year_error"])  # Ошибка: неверный формат года

    # Удаление книги
    elif current_state == CurrentStates.waiting_for_id_to_delete:
        book_id = message.text  # Получаем ID книги
        if library.delete_book(int(book_id)):  # Удаляем книгу
            await message.answer(MESSAGES["delete_success"])  # Сообщаем об успешном удалении
            await state.set_state(CurrentStates.waiting_for_click)  # Возвращаем в состояние ожидания действий
        else:
            await message.answer(MESSAGES["delete_fail"])  # Ошибка: книга не найдена

    # Изменение статуса книги
    elif current_state == CurrentStates.waiting_for_id_to_change:
        book_id_change = message.text  # Сохраняем ID книги
        if book_id_change.isnumeric():  # Проверяем, что ID корректен
            await state.set_state(CurrentStates.waiting_for_new_status)  # Состояние: ожидание нового статуса
            await message.answer(MESSAGES["status_prompt_new"])  # Запрос на ввод нового статуса
        else:
            await message.answer(MESSAGES["status_id_error"])  # Ошибка: неверный ID

    elif current_state == CurrentStates.waiting_for_new_status:
        status = message.text  # Получаем новый статус
        if status.lower() in ['выдана', 'в наличии']:  # Проверяем, что статус корректен
            if library.change_status(book_id=int(book_id_change), new_status=status):  # Изменяем статус книги
                await state.set_state(CurrentStates.waiting_for_click)  # Возвращаем в состояние ожидания действий
                await message.answer(MESSAGES["status_success"])  # Сообщаем об успешном изменении
            else:
                await message.answer(MESSAGES["status_fail"])  # Ошибка: книга не найдена
                await state.set_state(CurrentStates.waiting_for_click)  # Возвращаем в состояние ожидания действий
        else:
            await message.answer(MESSAGES["status_invalid"])  # Ошибка: неверный статус

    # Поиск книги
    elif current_state == CurrentStates.waiting_for_query:
        query = message.text  # Получаем поисковый запрос
        book = library.search_book(query)  # Ищем книгу
        if book is not None:
            await message.answer(str(book))  # Отправляем информацию о книге
            await state.set_state(CurrentStates.waiting_for_click)  # Возвращаем в состояние ожидания действий
        else:
            await message.answer(MESSAGES["search_not_found"])  # Ошибка: книга не найдена

    # Завершаем добавление книги
    if title and author and year:
        library.add_book(title, author, int(year))  # Добавляем книгу в библиотеку
        await message.answer(MESSAGES["add_success"])  # Сообщаем об успешном добавлении
        author, title, year = str(), str(), int()  # Сбрасываем временные данные


