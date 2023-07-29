from aiogram.fsm.state import State, StatesGroup


class FSM_main(StatesGroup):
    """
    Класс FSM_main представляет состояния (states) для работы с конечными автоматами (finite state machines).
    """

    genre = State()
    """
    Состояние genre - состояние выбора жанра.
    """

    search = State()
    """
    Состояние search - состояние поиска.
    """

    search_inline = State()
    """
    Состояние search_inline - состояние поиска встроенного (inline) запроса.
    """

    anime = State()
    """
    Состояние anime - состояние выбранного аниме.
    """

    description = State()
    """
    Состояние description - состояние описания аниме.
    """
