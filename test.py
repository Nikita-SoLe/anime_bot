from parse.scrap import anime_dict


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


def a():
    print(bin(-5))


if __name__ == "__main__":
    a()
