'''
2) Написать программу, которая собирает «Хиты продаж» с сайтов техники mvideo,
onlinetrade и складывает данные в БД. Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

'''

import time
import datetime
import itertools
import selenium
from selenium import webdriver          #Основной элемент
import pymongo
from pymongo import MongoClient
import pandas as pd

def hit_parser():
    driver = webdriver.Chrome()
    driver.get("https://www.mvideo.ru/")
    caro = driver.find_elements_by_css_selector('div.carousel-paging')
    caro_list = caro[2].find_elements_by_css_selector('a') #третья карусель это хиты продаж
    hit_all = []
    elem = driver.find_elements_by_class_name('sel-product-tile-title') #описание продукта

    for i in range (5):
        caro_list[i].click()
        time.sleep(2)
        elem = driver.find_elements_by_css_selector('a.sel-product-tile-title')
        time.sleep(3)
        hit = [x.text for x in elem][:4]
        hit_all.append(hit)
    return hit_all

def convert_to_mongo_dict(hit_all):
    merged_list = list(itertools.chain(*hit_all)) #объединяем все в общий список хиты продаж
    today_date = datetime.datetime.today()
    dates = [today_date for x in range(len(merged))]
    col  = ['date', 'title']
    df = pd.DataFrame(list(zip(dates, merged)), columns = col)
    df_dict = df.to_dict('records')
    return df_dict

def upload_mongodb(df):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['mvideo_hits']
    mvideo = db.mvideo_hits  # Имя коллекции
    mvideo.drop() #старую удаляем
    mvideo.insert_many(df)
    print(mvideo.count_documents({}))

upload_mongodb(df_dict)