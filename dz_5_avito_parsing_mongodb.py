
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import datetime
import pymongo
from pymongo import MongoClient

#Задание 1
#Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB
#и реализовать функцию, записывающую собранные объявления с avito.ru в созданную БД (xpath/BS для парсинга на выбор)


#Получаем доступ к авито
def request_to_site():
    try:
        request = requests.get('https://www.avito.ru/moskva_i_mo/doma_dachi_kottedzhi/sdam/dacha?cd=1')
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)

#Собираем данные по Московской области по аренде дач
def parse_avito():
    html_doc = request_to_site()
    soup = BeautifulSoup(html_doc, 'html.parser')
    try:
        title_news = soup.findAll('h3', {'class': 'title item-description-title'})  # заголовок и ссылка на новость
        currency = soup.findAll('span', attrs={'class': 'price'})  # цена и ссылка на новость
        address = soup.select("[data-marker =item-address]")  # расстояние
        time_text = soup.select('[data-marker =item-date]')  # дата


    except AttributeError:
        print("Нет данных")

    # Выбираем заголовки и создаем список цены
    title_list = [x.find('a').text for x in title_news]

    # Выбираем цену, форматируем ее в числа и создаем список цены
    price_list_raw = [x.find('span').parent.text for x in currency]
    price_list = [int(''.join(i for i in text if i.isdigit())) for text in price_list_raw]

    # Выбираем период оплаты и создаем список
    price_period = [text[-7:] for text in price_list_raw]

    # Выбираем валюту и создаем список валюты
    curr_list = [x.find('span').string for x in currency]

    # Выбираем время
    time_list = [x.text for x in time_text]
    time_list_f = []
    today_date = datetime.datetime.today()
    notoday_words = ['дня', 'день']  # список слов, которые указывают, что не сегодня

    for i in time_list:
        time_list_split = i.split()
        match = list(set(time_list_split) & set(notoday_words))  # сравниваем множества
        if len(match) == 0:  # если не совпадают, значит ставим сегодня
            today_date_r = datetime.datetime.date(today_date)
            time_list_f.append(today_date)
        else:
            day_time = int(re.findall(r'\b\d+\b', i)[0])  # получаем в список число и форматируем его
            date_r = datetime.datetime.now() - datetime.timedelta(days=day_time)  # вычисляем дельту времени
            date_u = datetime.datetime.date(date_r)  # переводим в формат год - мес - день
            time_list_f.append(date_u)

    # Выбираем расстояние, переводим в числа
    distance_list_raw = [x.text for x in address]
    distance_list_r = list(map(lambda sub: ''.join([ele for ele in sub if ele.isnumeric()]), distance_list_raw))
    distance_list_f = []
    # так как попадаются пробелы или нулевые расстояния, формируем новый список с учетом предела в Москве
    for i in distance_list_r:
        if len(i) > 0:
            distance_list_f.append(int(i))
        else:
            distance_list_f.append(0)

    # выбираем ссылки и создаем список
    b = 'https://www.avito.ru'
    link_list = [(b + x.find('a')['href']) for x in title_news]

    # делаем dataframe
    columns = ['description', 'price', 'period', 'km', 'date', 'curr', 'link']
    df = pd.DataFrame(
        list(zip(title_list, price_list, price_period, distance_list_f, time_list_f, curr_list, link_list)),
        columns=columns)

    return df.sort_values(by=['date'])  # вывод сортируем по дате


#Создаем базу в Mongodb и записываем в нее все данные

def upload_mongodb(df):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['avito_dacha']
    avito = db.avito_dacha  # Имя коллекции
    #avito.drop() #старую удаляем, если надо для проверки
    avito.insert_many(df)
    print(avito.count_documents({})) #считаем количество данных

#Задание 2

#Написать функцию, которая производит поиск и выводит на экран объявления с ценой меньше введенной суммы

def price_check(price_request):
    wanted_keys = ('description', 'price', 'period')
    dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y)])
    for b in avito.find().sort('price'):
        if b['price'] < price_request:
            print (dictfilt(b, wanted_keys))

#Задание 2 со звездочкой

# *Написать функцию, которая будет добавлять в вашу базу данных только новые объявления
# Добавляем новые записи проверяя по url

def update_date_newrecords(df):
    # Ищем последнюю дату записи в mongodb
    last_record_mongo = db.avito_dacha.find().sort('date', -1).limit(1)
    for i in last_record_mongo:
        last_date = i['date']

    # Выбираем данные из парсинга с более поздними датами, чем в mongodb
    new_dates = [i for i in df.date if i > last_date]

    # добавляем в mongodb записи с поледними датами
    for date in new_dates:
        df_raw = df.loc[df.date == date]
        df_raw_dict = df_raw.to_dict('records')
        avito.insert_one(df_raw_dict[0])

    print(avito.count_documents({}))