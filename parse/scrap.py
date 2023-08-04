import requests
import time
from bs4 import BeautifulSoup
import json

from database.db_buttons import genre, anime_dict


# Записывает главную страницу сайта
def read_anigo():
    url = 'https://animego.org/anime'

    page = requests.get(url)

    if page.status_code == 200:
        html = page.text

        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(html)


# Парсит жанры и ссылки на них с главной страницы
def scrap_genre():

    print('Start_scrap_genre')

    # Открываем записанный нами HTML документ главной страницы
    with open('parse/index.html', 'r', encoding='utf-8') as file:

        file = file.read()

        soup = BeautifulSoup(file, 'lxml')

        # Ищем все дивы по классу кнопок с жанрами
        divs = soup.find_all('span', class_='dropdown-item label cursor-pointer mb-0')

        dct = {}

        # Достаем название жанра и ссылку на него
        for div in divs:
            checkbox = div.find('input', class_='custom-control-input')
            data_text = checkbox['data-text']
            value = checkbox['value']
            dct[data_text] = {'url_value': value}

        # Записываем все это в .json
        with open('parse/genre.json', 'w', encoding='utf-8') as file_write:
            json.dump(dct, file_write, indent=4, ensure_ascii=False)

    print('Finish_scrap_genre')


# Обновляет файл с жанрами, добавляя к каждому жанру список с аниме.
# Записывает файл с базой об аниме
def scrap_anime():

    print('Start_scrap_anime')

    file = genre

    main_dct_anime = {}

    for key, value in file.items():

        print(key, value)
        dct_anime = {}

        flag = True
        count_page = 1

        name_anime = []

        while flag:

            url = f'https://animego.org/anime/filter/genres-is-{value["url_value"]}/apply?sort=createdAt&direction=desc&type=animes&page={count_page}'

            page = requests.get(url)
            html_code = page.text

            print(count_page)
            if page.status_code == 200:
                count_page += 1
                soup = BeautifulSoup(html_code, 'lxml')

                lst = soup.find_all('div', class_='h5 font-weight-normal mb-1')

                for item in lst:
                    # Достаем название Аниме
                    anime_name = item.find('a').text
                    # а тут ссылку на него
                    anime_url = item.find('a').get('href')

                    name_anime.insert(0, anime_name)

                    if anime_name not in main_dct_anime:
                        main_dct_anime[anime_name] = {'url': anime_url}

            else:
                flag = False

            time.sleep(0.5)

        dct_anime['name'] = name_anime

        file[key].update(dct_anime)

        # Записываем обновленный файл с жанрами
        with open('parse/genre.json', 'w', encoding='utf-8') as file_write:
            json.dump(file, file_write, indent=4, ensure_ascii=False)

    # Записываем новый файл с базой аниме
    with open('parse/anime.json', 'w', encoding='utf-8') as anime_write:
        json.dump(main_dct_anime, anime_write, indent=4, ensure_ascii=False)

    print('Finish_scrap_anime')


# Собирает данные об аниме
def scrap_description():

    print('Start_scrap_description')

    anime_db = anime_dict

    count = 1
    for key, value in anime_db.items():

        print(f'{key}: {count}/{len(anime_db)}')
        count += 1
        description = {}
        url = value['url']
        page = requests.get(url)

        time.sleep(0.3)
        html_code = page.text
        print(page.status_code)
        if page.status_code == 200:

            soup = BeautifulSoup(html_code, 'lxml')

            try:
                rating_value = soup.find('span', class_='rating-value').text
            except AttributeError as er:
                rating_value = 'Нет оценок'
                print(er)
            img = soup.find('div', class_='anime-poster position-relative cursor-pointer').find('img').get('src')

            lst_dt = soup.find('div', class_='anime-info').find_all('dt')
            lst_dd = soup.find('div', class_='anime-info').find_all('dd')

            description['Рейтинг'] = rating_value
            description['img'] = img

            for i, val in enumerate(lst_dt):
                text: str = val.text

                if text.strip() in ['Тип', 'Возрастные ограничения', 'Длительность']:
                    description[text.strip()] = lst_dd[i].text.strip()

        anime_db[key]['description'] = description

    with open('parse/anime.json', 'w', encoding='utf-8') as file:
        json.dump(anime_db, file, indent=4, ensure_ascii=False)

    print('Finish_scrap_description')


def start_scrap():
    scrap_genre()
    scrap_anime()
    scrap_description()


if __name__ == '__main__':
    scrap_description()
