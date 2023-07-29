import json


def get_genre() -> dict:
    with open('parse/genre.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


def get_anime_dict():
    with open('parse/anime.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


genre: dict = get_genre()
anime_dict: dict = get_anime_dict()