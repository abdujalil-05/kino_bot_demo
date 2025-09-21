from aiogram.fsm.state import State, StatesGroup


class AddMovieState(StatesGroup):
    movie_name = State()
    movie_year = State()
    movie_language = State()
    movie_genres = State()
    movie_url = State()
    movie_description = State()
    movie_rating = State()


class DeleteMovieState(StatesGroup):
    movie_id = State()