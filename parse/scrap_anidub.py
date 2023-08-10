import requests
import time
from bs4 import BeautifulSoup
import json


def read_anidub():
    url = 'https://animedub.ru/anime'

    page = requests.get(url)

    if page.status_code == 200:
        html = page.text

        with open('anidub.html', 'w', encoding='utf-8') as file:
            file.write(html)


def scrap_genre():

    genre = {}

    with open('anidub.html', 'r', encoding='utf-8') as file:

        file = file.read()

        soup = BeautifulSoup(file, 'lxml')

        divs = soup.find('div', class_='sidebar').find('ul').find_all('li')

        for item in divs:

            href = item.find('a')['href']
            name = item.text

            genre[name] = {'url': href}

    with open('database/anidub.json', 'w', encoding='utf-8') as file:
        json.dump(genre, file, ensure_ascii=False, indent=4)


def get_anidub_genres() -> dict:
    with open('database/anidub.json', 'r', encoding='utf-8') as file:
        genres = json.load(file)
        return genres


def scrap_anime():
    genres = get_anidub_genres()
    anime_dict_bd = {}

    for name in genres.keys():

        flag = True
        page = 1
        name_anime = []
        while flag:
            print(f"Name: {name}\nPage_num: {page}")

            url = f'https://animedub.ru{genres[name]["url"]}page/{page}/'

            page_get = requests.get(url)
            html_code = page_get.text

            time.sleep(0.3)

            print(page_get.status_code)
            if page_get.status_code == 200:
                page += 1
                soup = BeautifulSoup(html_code, 'lxml')

                lst_names = soup.find_all('a', class_='mov-t nowrap')

                for name_a in lst_names:

                    href = name_a.get('href')
                    title = name_a.find('h2').text.split('/')[0]

                    name_anime.append(title)

                    if title not in anime_dict_bd:
                        anime_dict_bd[title] = {'url': href}
            else:
                flag = False

        genres[name] = {'name': name_anime}
        print(genres[name])

    with open('database/anidub.json', 'w', encoding='utf-8') as file:
        json.dump(genres, file, indent=4, ensure_ascii=False)

    with open('database/anidub_anime_db.json', 'w', encoding='utf-8') as file:
        json.dump(anime_dict_bd, file, indent=4, ensure_ascii=False)


def get_anidub_bd() -> dict:
    with open('../database/anidub_anime_db.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def scrap_description():

    anime_db = get_anidub_bd()

    count = 1
    for key, value in anime_db.items():

        print(f'{key}: {count}/{len(anime_db)}')
        count += 1

        description = {}

        url = value['url']
        page = requests.get(url)

        time.sleep(0.1)
        html_code = page.text
        print(page.status_code)

        if page.status_code == 200:

            soup = BeautifulSoup(html_code, 'lxml')

            try:
                rating_value = soup.find('div', class_='r-imdb').text
            except AttributeError as er:
                rating_value = "Нет оценок"
                print(er)

            img = soup.find('picture').find('img').get('src')
            img = f"https://animedub.ru{img}"

            description['Рейтинг'] = rating_value
            description['img'] = img

            lst_li = soup.find('ul', class_='mov-list').find_all('li')

            for item in lst_li:

                item_text = item.find('div', class_='mov-label').text

                if item_text == 'Год выхода':
                    description['Год выхода'] = item.find('a').text
                elif item_text == 'Страна':
                    description['Страна'] = item.find('span').text
                elif item_text == 'Количество серий':
                    tipe: str = item.find('span').text.split()[0]
                    if tipe.isalpha():
                        if tipe == 'ТВ':
                            description['Тип'] = 'ТВ Сериал'
                        else:
                            description['Тип'] = tipe
                    elif tipe.isdigit() or tipe == '??':
                        description['Тип'] = 'ТВ Сериал'

        print(description)
        anime_db[key]['description'] = description

    with open('database/anidub_anime_db.json', 'w', encoding='utf-8') as file:
        json.dump(anime_db, file, indent=4, ensure_ascii=False)



if __name__ == "__main__":
    scrap_description()