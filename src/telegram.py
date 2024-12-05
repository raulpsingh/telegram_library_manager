from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from src import keyboards
from src.library import Library
from src.messages import MESSAGES
from src.states import CurrentStates

author, title, year = str(), str(), int()  # Временные переменные для данных книги
book_id_change = int()  # ID книги для изменения её статуса

# Инициализация бота и библиотеки
router = Router()  # Маршрутизатор для управления командами
library = Library()  # Экземпляр библиотеки для работы с книгами


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    """Обработчик команды /start. Показывает меню с кнопками."""
    await state.set_state(CurrentStates.waiting_for_click)
    await message.answer("Hello", reply_markup=keyboards.keyboard())


@router.message(F.text == 'Добавить книгу')
async def add_book_button(message: types.Message, state: FSMContext):
    """Начало процесса добавления книги."""
    await state.set_state(CurrentStates.waiting_for_book_title)
    await message.answer(MESSAGES["add_prompt_title"])


@router.message(F.text == 'Изменить статус')
async def change_status_button(message: types.Message, state: FSMContext):
    """Начало изменения статуса книги."""
    await state.set_state(CurrentStates.waiting_for_id_to_change)
    await message.answer(MESSAGES["status_prompt_id"])


@router.message(F.text == "Удалить книгу")
async def delete_book_button(message: types.Message, state: FSMContext):
    """Начало удаления книги."""
    await state.set_state(CurrentStates.waiting_for_id_to_delete)
    await message.answer(MESSAGES["delete_prompt_id"])


@router.message(F.text == 'Найти книгу')
async def search_book_button(message: types.Message, state: FSMContext):
    """Начало поиска книги."""
    await state.set_state(CurrentStates.waiting_for_query)
    await message.answer(MESSAGES["search_prompt"])


@router.message(F.text == 'Показать все книги')
async def display_books_button(message: types.Message):
    """Выводит список всех книг в библиотеке."""
    if library.books:
        for book in library.books:
            await message.answer(str(book))
    else:
        await message.answer(MESSAGES["no_books"])


@router.message(F.text)
async def handle_input(message: types.Message, state: FSMContext):
    """Обрабатывает действия для разных состояний."""
    global author, title, year, book_id_change
    current_state = await state.get_state()

    if current_state == CurrentStates.waiting_for_book_title:
        title = message.text
        await state.set_state(CurrentStates.waiting_for_book_author)
        await message.answer(MESSAGES["add_prompt_author"])

    elif current_state == CurrentStates.waiting_for_book_author:
        author = message.text
        await state.set_state(CurrentStates.waiting_for_book_year)
        await message.answer(MESSAGES["add_prompt_year"])

    elif current_state == CurrentStates.waiting_for_book_year:
        if message.text.isnumeric():
            year = message.text
            library.add_book(title, author, int(year))
            await state.set_state(CurrentStates.waiting_for_click)
            await message.answer(MESSAGES["add_success"])
            author, title, year = str(), str(), int()
        else:
            await message.answer(MESSAGES["add_year_error"])

    elif current_state == CurrentStates.waiting_for_id_to_delete:
        if library.delete_book(int(message.text)):
            await message.answer(MESSAGES["delete_success"])
        else:
            await message.answer(MESSAGES["delete_fail"])
        await state.set_state(CurrentStates.waiting_for_click)

    elif current_state == CurrentStates.waiting_for_id_to_change:
        if message.text.isnumeric():
            book_id_change = int(message.text)
            await state.set_state(CurrentStates.waiting_for_new_status)
            await message.answer(MESSAGES["status_prompt_new"])
        else:
            await message.answer(MESSAGES["status_id_error"])

    elif current_state == CurrentStates.waiting_for_new_status:
        status = message.text.lower()
        if status in ['выдана', 'в наличии']:
            if library.change_status(book_id=book_id_change, new_status=status):
                await message.answer(MESSAGES["status_success"])
            else:
                await message.answer(MESSAGES["status_fail"])
        else:
            await message.answer(MESSAGES["status_invalid"])
        await state.set_state(CurrentStates.waiting_for_click)

    elif current_state == CurrentStates.waiting_for_query:
        query = message.text
        book = library.search_book(query)
        if book:
            await message.answer(str(book))
        else:
            await message.answer(MESSAGES["search_not_found"])
        await state.set_state(CurrentStates.waiting_for_click)
