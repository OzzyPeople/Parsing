
''''

Задание 1. Доработать приложение по поиску авиабилетов, чтобы оно возвращало билеты по названию города,
а не по IATA коду. Пункт отправления и пункт назначения должны передаваться в качестве параметров.
Сделать форматированный вывод, который содержит в себе пункт отправления, пункт назначения, дату вылета,
цену билета (можно добавить еще другие параметры по желанию)

'''

import json
import requests
import pandas as pd

#Подключимся к API http://airlabs.co/api/v6/airports?api_key=  и сделаем словарь - код IATA - город

re1 = requests.get("http://airlabs.co/api/v6/cities?api_key=0d18c69c-ac96-4097-a920-3272ba1cfe76&lang=en")
cities = re1.json()
iata_codes1 = cities['response']

#Сделаем словарь с ключом iata и значением города
codes_iata =[]
cities_iata =[]
for i in iata_codes1:
    for b in i:
        if b == 'code':
            codes_iata.append(i[b])
        if b == 'name':
            cities_iata.append(i[b])

code_city = {k: v.lower() for (k, v) in zip(codes_iata, cities_iata)}

#Так как по API есть только 10000 аэропортов, но нет Москвы и Нью Йорка, добавим их вручную

code_city['MOW'] = "moscow"
code_city['NYC'] = "new york"

#Введем переменные городов вылета и прилета


city_origin = input ('Введите город вылета на английском языке ').lower()
city_destin = input ('Введите город прилета на английском языке ').lower()
city_origin_iata = str()
city_destin_iata = str()

for i, k in code_city.items():
    if k == city_origin:
        city_origin_iata = i
    if k == city_destin:
        city_destin_iata = i
if len(city_origin_iata) ==0:
        print ('такого города в списке вылета нет')
if len(city_destin_iata) ==0:
        print ('такого города в списке прилета нет')

#Подключимся к API aviasales и структурируем данные

flight_params = {
    'origin': city_origin_iata,
    'destination': city_destin_iata,
    'one_way': 'false'
}
req = requests.get("http://min-prices.aviasales.ru/calendar_preload", params=flight_params)
data = req.json()

value = []
depart_date = []
return_date = []
gate = []
fields = ['origin', 'departure','gate', 'depart_date', 'return_date', 'value']
for i in data['best_prices']:
    for k in i:
        if k == 'value':
            value.append(i[k])
        if k == 'depart_date':
            depart_date.append(i[k])
        if k == 'return_date':
            return_date.append(i[k])
        if k == 'gate':
            gate.append(i[k])

#Создаем список городов вылета и прилета по длине полученных данных
origin = [city_origin for x in range(len(value))]
destination = [city_destin for x in range(len(value))]
total = [origin, destination, gate, depart_date, return_date, value]
flyd = dict(zip(fields, total)) #объединим в словарь все данные

#Создадим data frame и выведим топ 10 в отсортированном виде по цене и дате прилета

dd = pd.DataFrame.from_dict(flyd)
dd.sort_values(by=['value', 'depart_date']).head(10)
