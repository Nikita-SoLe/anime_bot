import json


def get_genre() -> dict:
    with open('database/anidub.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


def get_anime_dict() -> dict:
    with open('database/anidub_anime_db.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


def get_feature() -> dict:
    with open('database/feature.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


def get_serials() -> dict:
    with open('database/serials.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


def get_OVA() -> dict:
    with open('database/OVA.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


def get_special() -> dict:
    with open('database/special.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        return file


def get_anime_dict() -> dict:
    with open('database/anidub_anime_db.json', 'r', encoding='utf-8') as file:
        return json.load(file)


anime_dict: dict = get_anime_dict()
genre: dict = get_genre()
feature_film: dict = get_feature()
serials: dict = get_serials()
OVA: dict = get_OVA()
specials: dict = get_special()

