import json

from database.db_buttons import anidub_db, anime_dict
from utils.get_description_anime import get_ranting


def sum_a():

    count_serial = 0
    count_ONA = 0
    count_movie = 0
    count_special = 0
    count_OVA = 0
    count_korotko = 0

    for key in anidub_db.keys():

        if anidub_db[key]['description']:
            if 'Тип' in anidub_db[key]['description']:
                type_ = anidub_db[key]['description']['Тип']
                if type_ == "ТВ Сериал":
                    count_serial += 1
                elif type_ in ["ONA"]:
                    count_ONA += 1
                elif type_ == 'OVA':
                    count_OVA += 1
                elif type_ in ["Фильм"]:
                    count_movie += 1
                elif type_ == 'Спешл':
                    count_special += 1
                elif type_ in ['Короткометражный', 'Короткометражное']:
                    count_korotko += 1

    print(f'Serial : {count_serial}\n'
          f'Movie : {count_movie}\n'
          f'OVA : {count_OVA}\n',
          f'ONA : {count_ONA}\n',
          f'Коротко : {count_korotko}\n',
          f'Спешл : {count_special}')


def count_char():

    count = 0
    for name in anidub_db.keys():
        count += len(name)

    print(count)


def sorted_top_50():

    top_50_value = [['', 0]] * 50

    for name in anime_dict:
        rating = get_ranting(name)
        if rating != "Не доступно":
            rating = float(get_ranting(name).replace(',', '.'))

            if rating > top_50_value[-1][-1]:
                top_50_value.insert(0, [name, rating])
                top_50_value.sort(reverse=True, key=lambda x: x[1])
                top_50_value.pop(-1)

    with open('database/top_50_of_all.json', 'w', encoding='utf-8') as file:
        json.dump(top_50_value, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    sorted_top_50()