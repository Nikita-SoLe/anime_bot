import json


def get_genre() -> dict:
    with open('parse/genre.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


def get_anime_dict():
    with open('parse/anime.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


def get_feature():
    with open('database/feature.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


def get_serials():
    with open('database/serials.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


def get_OVA():
    with open('database/OVA.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


def get_special():
    with open('database/special.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


genre: dict = get_genre()
anime_dict: dict = get_anime_dict()
feature_film: dict = get_feature()
serials: dict = get_serials()
OVA: dict = get_OVA()
specials: dict = get_special()
