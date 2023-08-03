from database.db_buttons import anime_dict


def get_ranting(name: str) -> str:
    if "Рейтинг" in anime_dict[name]["description"]:
        ranting = anime_dict[name]['description']['Рейтинг']
        return ranting
    return 'Не доступно'


def get_name_text_clipping(name: str) -> str:
    return name[:35]
