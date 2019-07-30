'''
2) Доработать приложение таким образом,
чтобы можно было искать разработчиков на разные языки программирования (Например Python, Java, C++)
'''

import requests
from lxml import html

url_r = 'https://hh.ru/search/resume?'

def parse_hh_res(url1):
    my_str = input('Введите язык программирования ')
    area = int(input('Введите номер региона '))  # Москва 1
    pages = int(input('Введите количество страниц '))
    period = int(input('Введите количество дней для парсинга '))
    headers = {'accept': '*/*',
               'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    for i in range(pages):
        params = {'text': my_str, 'period': period, 'per_page':'10', 'logic': 'normal', 'clusters': True, 'area': area, 'page':i, 'pos': 'full_text', 'exp_period': ''}
        session = requests.Session()  # открываем сессию пользователя
        request = session.get(url1, params=params, headers=headers)
        if request.status_code == 200:
            root = html.fromstring(request.text)
            resumes = root.xpath("//div[contains(@class, 'resume-search-item__header')]")
            for resume in resumes:
                print(resume.xpath('.//a/text()')[0])
                b = resume.xpath('.//a/@href')[0]
                print(f'hh.ru{b}')
                try:
                    print(resume.xpath('.//div[contains(@class, "item__compensation")]/text()')[0])
                except IndexError:
                    print('Нет данных')
                print('-' * 25)
        else:
            print('error')

parse_hh_res(url_r)