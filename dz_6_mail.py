from selenium import webdriver          #Основной элемент
from selenium.webdriver.common.keys import Keys    #Клавиши клавиатуры

'''
1) Написать программу, которая собирает входящие письма из своего или тестового 
почтового ящика и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма)

'''
#Для борьбы с ошибками
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import pymongo
from pymongo import MongoClient


def parsing_email_mail_ru(login, password):
    driver = webdriver.Chrome()
    driver.get('https://mail.ru/')
    assert "Mail.ru" in driver.title
    wait = WebDriverWait(driver, 50)
    # Заполняем поля для ввода
    elem = driver.find_element_by_id("mailbox:login")
    elem.send_keys(login)
    elem = driver.find_element_by_id("mailbox:password")
    elem.send_keys(password_)
    elem.send_keys(Keys.RETURN)
    time.sleep(5)
    # Собираем темы писем
    title = driver.find_elements_by_css_selector('a.llc div.llc__container .llc__item.llc__item_title')
    time.sleep(5)
    # Собираем всех отправителей
    sender = driver.find_elements_by_css_selector('span.ll-crpt')
    time.sleep(5)
    sender_list = [x.text for x in sender]
    # Собираем даты писем
    date = driver.find_elements_by_xpath('//div[@class ="llc__item llc__item_date"]')
    time.sleep(5)
    title_list = [x.text for x in title]
    date_list = [x.text + ' 2019' for x in date]
    # собираем ссылки на все письма, а не элементы
    email_links = driver.find_elements_by_xpath("//a[contains(@class, 'js-tooltip-direction_letter-bottom')]")
    email_links_list = [x.get_attribute('href') for x in email_links]
    body_text_list = []
    time.sleep(5)
    # проходимся по каждой ссылке и собираем тексты писем
    for i in email_links_list:
        try:
            driver.get(i)
            time.sleep(5)
            body_text = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@class="letter__body"]')))
            time.sleep(5)
            body_text_list.append(body_text.text)

        except TimeoutException:
            print("Timeout exception case")

        except NoSuchElementException:
            print("NoSuchElementException case")

    cols = ['sender', 'date', 'title', 'text']
    df = pd.DataFrame(list(zip(sender_list, date_list, title_list, body_text_list)), columns=cols)
    return (df)

def upload_mongodb(df):
    df_dict = df.to_dict('records')
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['emails']
    emails = db.emails  # Имя коллекции
    emails.drop() #старую удаляем
    emails.insert_many( df_dict)
    print(emails.count_documents({}))

login = 'marko_polo_81@bk.ru'
password_ = 'Wz#z2z1eBTkt'

upload_mongodb(parsing_email_mail_ru(login, password_))

