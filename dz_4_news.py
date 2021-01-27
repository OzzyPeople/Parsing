import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import datetime

'''
1) С помощью BeautifulSoup спарсить новости с https://news.yandex.ru по своему региону.

*Заголовок - ок 
*Краткое описание ок
*Ссылка на новость - ок 
2) * Разбить новости по категориям - ок
* Расположить в хронологическом порядке

'''

def request_to_site():
    headers = {
        'accept': '*/*',
         'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    params = {
        'text': 'Программист'
    }
    try:
        request = requests.get('https://news.yandex.ru/Moscow_and_Moscow_Oblast/index.html', headers=headers)
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


def convert_time(listik):
    today_date = datetime.datetime.today().strftime("%Y/%m/%d")

    yesterday_date_full = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday_before_date_full = datetime.datetime.now() - datetime.timedelta(days=2)

    yesterday_date = yesterday_date_full.strftime("%Y/%m/%d")
    yesterday_before = yesterday_before_date_full.strftime("%Y/%m/%d")

    word1 = 'вчера'
    word2 = 'июля'

    date_list = []

    for i in listik:
        if word1 in i:
            date_i = yesterday_date + " " + i[-5:]
            date_list.append(date_i)
        if word2 in i:
            date_b = yesterday_before + " " + i[-5:]
            date_list.append(date_b)
        else:
            date_k = today_date + " " + i[-5:]
            date_list.append(date_k)

    date_list_format = []

    for d in date_list:
        date_time_obj = datetime.datetime.strptime(d, '%Y/%m/%d %H:%M')
        date_list_format.append(date_time_obj)

    return sorted(date_list_format, reverse=True)


def parse_news():
    html_doc = request_to_site()
    soup = BeautifulSoup(html_doc, 'html.parser')
    # allnewstext = soup.findAll('h2', {'class': 'story__title'})
    try:
        title_news = soup.findAll('h2', {'class': 'story__title'})  # заголовок и ссылка на новость
        text_news = soup.find_all('div', attrs={'class': 'story__text'})
        newsdates = soup.find_all('div', attrs={'class': 'story__date'})

    except AttributeError:
        print("Нет данных")

    regex = re.compile('.*label_top*.')
    labels = soup.find_all('a', {'class': regex})
    title_list = [x.find('a').string for x in title_news]
    label_list = [x.get_text() for x in labels]
    text_news = [x.text for x in text_news]

    # выбирае ссылки
    b = 'https://news.yandex.ru'
    link_list = [(b + x.find('a')['href']) for x in title_news]

    # ищем время и форматируем его
    date_list = [x.text for x in newsdates]
    date_list_format = convert_time(date_list)

    # делаем dataframe
    columns = ['Заголовок', 'Рубрика', 'Время', 'Текст', 'Ccылка']
    df = pd.DataFrame(list(zip(title_list, label_list, date_list_format, text_news, link_list)), columns=columns)

    return df.sort_values(by=['Время'])

parse_news()