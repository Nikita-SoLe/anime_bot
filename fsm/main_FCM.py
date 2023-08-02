from aiogram.fsm.state import State, StatesGroup


class FSM_main(StatesGroup):
    """
    Класс FSM_main представляет состояния (states) для работы с конечными автоматами (finite state machines).
    """
    genre = State()
    search = State()
    feature_film = State()
    serials = State()
    OVA = State()
    specials = State()


class Genre(StatesGroup):

    anime = State()
    description = State()


class Search(StatesGroup):
    search_inline = State()


class FeatureFilm(StatesGroup):

    anime = State()
    description = State()


class Serials(StatesGroup):

    anime = State()
    description = State()


class OVA_State(StatesGroup):

    anime = State()
    description = State()


class Specials(StatesGroup):

    anime = State()
    description = State()
