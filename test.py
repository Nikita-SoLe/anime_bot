import json

from parse.scrap import anime_dict, genre


def sum_a():

    count_serial = 0
    count_ONA = 0
    count_movie = 0
    count_OVA = 0
    count_special = 0

    for key in anime_dict.keys():

        if anime_dict[key]['description']:
            type_ = anime_dict[key]['description']['Тип']
            if type_ == "ТВ Сериал":
                count_serial += 1
            elif type_ == "ONA":
                count_ONA += 1
            elif type_ == "Фильм":
                count_movie += 1
            elif type_ == "OVA":
                count_OVA += 1
            elif type_ == "Спешл":
                count_special += 1

    print(f'Serial : {count_serial}\n'
          f'Movie : {count_movie}\n'
          f'OVA : {count_OVA + count_ONA}\n'
          f'Special : {count_special}')


def write_genre_film():

    feature_film = {}
    serials = {}
    OVA = {}
    special = {}

    for key in genre.keys():
        lst_feature = []
        lst_serials = []
        ova_lst = []
        special_lst = []
        for name in genre[key]['name']:
            print(name)
            if name in anime_dict:
                if anime_dict[name]['description']:
                    type_ = anime_dict[name]['description']['Тип']
                    if type_ == "ТВ Сериал":
                        lst_serials.append(name)
                    elif type_ == "ONA" or type_ == "OVA":
                        ova_lst.append(name)
                    elif type_ == "Фильм":
                        lst_feature.append(name)
                    elif type_ == "Спешл":
                        special_lst.append(name)

        feature_film[key] = lst_feature
        serials[key] = lst_serials
        OVA[key] = ova_lst
        special[key] = special_lst

    with open('database/feature.json', 'w', encoding='utf-8') as file:
        json.dump(feature_film, file, indent=4, ensure_ascii=False)

    with open('database/serials.json', 'w', encoding='utf-8') as file:
        json.dump(serials, file, indent=4, ensure_ascii=False)

    with open('database/OVA.json', 'w', encoding='utf-8') as file:
        json.dump(OVA, file, indent=4, ensure_ascii=False)

    with open('database/special.json', 'w', encoding='utf-8') as file:
        json.dump(special, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    write_genre_film()