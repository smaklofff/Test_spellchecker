
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
    while len(href_list) < 15000:
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
