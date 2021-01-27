
'''
1) Необходимо собрать информацию о вакансиях на должность программиста или разработчика с сайта job.ru или hh.ru.
(Можно с обоих сразу) Приложение должно анализировать несколько страниц сайта. Получившийся список должен содержать в себе:

*Наименование вакансии,
*Предлагаемую зарплату
*Ссылку на саму вакансию

'''

url = 'https://hh.ru/search/vacancy?'


def parse_hh1(url):
    my_str = input('Введите должность ')
    area = int(input('Введите номер региона '))  # Москва
    pages = int(input('Введите количество страниц для парсинга '))
    period = int(input('Введите количество дней для парсинга'))
    headers = {'accept': '*/*',
               'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    for i in range(pages):
        params = {'text': my_str, 'period': period, 'per_page': '10', 'area': area, 'page': i}
        session = requests.Session()  # открываем сессию пользователя
        request = session.get(url, params=params, headers=headers)
        if request.status_code == 200:
            root = html.fromstring(request.text)
            vacancies = root.xpath("//div[contains(@class, 'item__row_header')]")
            for vacancy in vacancies:
                print(vacancy.xpath('.//a/text()')[0])
                print(vacancy.xpath('.//a/@href')[0])
                try:
                    print(vacancy.xpath('.//div[contains(@class, "item__compensation")]/text()')[0])
                except IndexError:
                    print('Нет данных')
                print('-' * 25)
        else:
            print('error')