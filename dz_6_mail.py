from selenium import webdriver          #Основной элемент
from selenium.webdriver.common.keys import Keys    #Клавиши клавиатуры

'''
1) Написать программу, которая собирает входящие письма из своего или тестового 
почтового ящика и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма)

'''

driver = webdriver.Chrome()
driver.get('https://mail.ru/')
assert "Mail.ru" in driver.title

#Заполняем поля для ввода
elem = driver.find_element_by_id("mailbox:login")
elem.send_keys('marko_polo_81@bk.ru')
elem = driver.find_element_by_id("mailbox:password")
elem.send_keys('Wz#z2z1eBTkt')
elem.send_keys(Keys.RETURN)

'''
Дальше не получилось, пробовал разные варианты:

elem = driver.find_element_by_css_selector('a.llc div.llc__container .llc__item.llc__item_title').text

не видит

'''