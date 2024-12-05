from aiogram.fsm.state import State, StatesGroup


class CurrentStates(StatesGroup):
    waiting_for_click = State()
    waiting_for_book_title = State()
    waiting_for_book_author = State()
    waiting_for_book_year = State()
    waiting_for_book_search = State()
    waiting_for_id_to_delete = State()
    waiting_for_id_to_change = State()
    waiting_for_new_status = State()
    waiting_for_query = State()
