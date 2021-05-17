import csv
from threading import Thread
import wikipedia
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from threading import Thread
import pandas as pd
import pymorphy2
import math


def _csv_writer(data, path):    # Записывает данные в csv файл
    frame = pd.DataFrame(data)
    frame.to_csv(path, index=False)


def tokenizer(text):    # Токенизатор
    vectorizer = TfidfVectorizer()
    bag_of_words = vectorizer.fit_transform(text)
    _csv_writer(text, 'Standart_text.txt')  # Сохранение сырого текста
    _csv_writer(start_auxiliary_threads(vectorizer.get_feature_names()), 'data3.csv')   # Сохранение чистого текста
    return len(vectorizer.get_feature_names())


def _clean(data, clean_list):   # Очищает полученные данные
    morph = pymorphy2.MorphAnalyzer()
    for wrd in data:
        if morph.word_is_known(wrd):
            normal_form_wrd = morph.parse(wrd)[0]
            clean_list.extend([normal_form_wrd.lexeme[i].word for i in range(len(normal_form_wrd.lexeme))])


def _get_text(data, text):  # Получение текстовой информации из статей вики
    wikipedia.set_lang("ru")
    for title in data:
        try:
            text.append(re.compile('[^а-яА-Я ]').sub('', wikipedia.page(title).content))
            print(title)
        except:
            print("Страница перенаправляет на другие статьи")


def start_auxiliary_threads(data):  # Подключение нескольких потоков, чтобы ускорить процесс получения данных
    clean_list = []

    batch_size = 0
    for i in range(32):
        flow = Thread(target=_clean, args=[data[batch_size:batch_size+100], clean_list])
        flow.start()
        batch_size += 100
    for i in range(32):
        flow.join()

    return sorted(set(clean_list))


def start_main_threads(data):   # Подключение нескольких потоков, чтобы ускорить процесс получения данных
    text = []

    batch_size = 0
    for i in range(32):
        flow = Thread(target=_get_text, args=[data[batch_size:batch_size + 10], text])
        flow.start()

        batch_size += 10

    for i in range(32):
        flow.join()

    return text


if __name__ == "__main__":
    with open('data2.csv', newline='', encoding='utf-8') as f:  # Получение данных из предыдущей программы
        reader = csv.reader(f)
        data = list(reader)

    print(tokenizer(start_main_threads(data)))
