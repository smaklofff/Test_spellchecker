"""
    Задание:
    1. Скачать все тексты всех статей русскоязычной википедии
    2. Сохранить все уникальные словоформы всех слов ( т.е. рыба, рыбы, рыбу, рыбам, рыбой и т.д. ) в словарь.
    3. При проверке орфографии, считать слово ошибочным, если оно не присутствует в словаре

    Немного о решении задачи:
    Для каждого пункта из задания была создана собственная программа. Это сделано для того, чтобы упростить тестирование.

    Первая программа (то есть та, в которой находится этот текст) выполняет роль сборщика названий статей.
    Вторая программа (Parser_2.py) использует данные, полученные из Parser_1.py, чтобы с помощью API Wiki получить текст
    со страницы, а потом обработать
    Третья программа получает результаты выполнения Parser_2.py и на основе этих данных строит модели для проверки
    орфографии.

"""
"""
    Возможности для улучшения:
    1) Использовать многопоточность или асинхронное программирование
    
"""
import requests
import bs4
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import lxml
import csv
import pandas as pd


def _link_list(block):  # Собирает из основного блока wiki все названия статей
    for a_tag in block.findAll("a"):
        name = a_tag.text
        href_list.append(name)


def _main(link):  # Переходит на страницы, где есть названия статей
    while len(href_list) < 1000:
        response = requests.get(link)
        link = 'https://ru.wikipedia.org/'
        soup = BeautifulSoup(response.text, 'lxml')
        block = soup.find('ul', class_='mw-allpages-chunk')
        _link_list(block)
        link = urljoin(link, soup.find('div', class_='mw-allpages-nav').contents[-1].attrs['href'])


def _csv_writer(data, path):  # Записывает данные в csv файл
    frame = pd.DataFrame(data)
    frame.to_csv(path, index=False)


if __name__ == "__main__":
    href_list = []
    _main('https://ru.wikipedia.org/w/index.php?title=Служебная:Все_страницы&hideredirects=1')
    _csv_writer(href_list, 'data2.csv')
