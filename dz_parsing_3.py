import json
import requests
import pandas as pd
from collections import defaultdict
import re
import collections
import lxml.html
import io

'''

Задание 3.*Научить приложение определять количество ссылок в статье. 
Спарсить каждую ссылку и результаты записать в отдельные файлы.

'''

url = 'https://www.finam.ru/'


# читаем html страницу и выводим текст

def pars_html(url):
    url_request = requests.get(url)
    return url_request


def read_record(url):
    # надо взять домен из url
    domain_name = re.sub(r'(.*://)?([^/?]+).*', '\g<1>\g<2>', url)

    # читаем текст
    response_text = pars_html(url).text

    # находим дерево
    dom = lxml.html.fromstring(response_text)
    # выбираем ссылки на только интересующий нас домен

    list_urls_0 = [x for x in dom.xpath('//a/@href') if '//' in x and domain_name in x]
    list_urls_1 = set() #множество ссылок, которые мы получили с первой ссылки
    j = 'http:'
    k = 'https:'
    for url in list_urls_0:
        if (url.lower().startswith(j) == False and url.lower().startswith(k) == False):
            b = f'{j}{url}' #дополняем битые ссылки, чтобы избежать ошибку Missing Schema
            list_urls_1.add(b)
        else:
            list_urls_1.add(url)
    return list_urls_1

#Запишем данные с каждой ссылки в отдельный файл

def find_att(list_urls_1):
    counter = 0
    for url in list_urls_1:
        res = requests.get(url)
        b = res.text
        counter+=1
        with io.open('file_{0}.txt'.format(counter),'w', encoding='utf-8') as file:
            file.write(b)
            file.close()

# Запускаем cбор ссылок
n = read_record (url)
# определяем количество ссылок
len(n)
# записываем данные из каждой ссылки в отдельный файл
find_att(n)