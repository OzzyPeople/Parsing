'''

Задание 2. В приложении парсинга википедии получить
первую ссылку на другую страницу и вывести все значимые слова из неё.
Результат записать в файл в форматированном виде


'''

import json
import requests
import re
import collections
import lxml.html

# В качестве первой страницы возьмем биографию Наполеона
url = 'https://ru.wikipedia.org/wiki/%D0%9D%D0%B0%D0%BF%D0%BE%D0%BB%D0%B5%D0%BE%D0%BD_I'


#читаем html страницу и выводим текст
def return_wiki_html(url):
    wiki_request = requests.get(url)
    return wiki_request.text

#выводим список ссылок и берем первую
def get_1st_link(response):
    dom = lxml.html.fromstring(response)
    list_urls = [x for x in dom.xpath('//a/@href') if '//' in x and 'ru.wikipedia.org' in x]
    return list_urls[0]

#выводим список наиболее частотных слов из первой ссылки, которую получили с парсинга первой страницы
def count_words (url):
    first_wiki_html = return_wiki_html(url)
    first_url_wiki = get_1st_link(first_wiki_html)
    second_wiki_html = return_wiki_html(first_url_wiki)
    words = re.findall('[A-Za-z]{4,}', second_wiki_html) #ищем символы на английском языке
    words_counter = collections.Counter()
    for word in words:
        words_counter[word] += 1
    for word in words_counter.most_common(10):
        print(f'Слово {word[0]} встречается {word[1]} раз')
    return words_counter.most_common(10)

print (count_words (url))