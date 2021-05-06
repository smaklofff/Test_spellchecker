"""
    Задание:
    1. Скачать все тексты всех статей русскоязычной википедии
    2. Сохранить все уникальные словоформы всех слов ( т.е. рыба, рыбы, рыбу, рыбам, рыбой и т.д. ) в словарь.
    3. При проверке орфографии, считать слово ошибочным, если оно не присутствует в словаре

    Пути решения проблемы:
    Есть 2 способа (которые я нашел) скачать все тексты из русской вики:
    1) Обратиться к базам данных вики и скачать все тексты
    2) Собрать все тексты с помощью программы

    Первый способ позволяет скачать данные за короткий срок, но полученные данные занимают очень много места, также
    в файле есть ошибка, которая не позволяет распаковать его (возможно ошибка только в этом файле, так как похожий
    файл, но со страницами на английском, не выдал ошибку)
    Также данный способ не подходит под требование предоставить 'код решения (включая получение данных)'

    Второй способ более медленный, но нет проблем первого способа

    Ниже представлен код, который использует 2 способ получения данных
"""



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
        """
            В строке ниже происходит проверка на существование слова с помощью популярной библиотеки pymorphy2.
            Минусы данного метода:
                1) При появлении новых слов в вики, программа все равно будет думать, что такого слова нет
            Плюсы:
                1) Слова, которые написаны неправильно или не существуют, не будут учитываться
            
            Альтернативные варианты решения:
            
            Если предположить, что ошибки в больших текстах встречаются реже, чем значимые слова, то можно подобрать
            такой фильтр, который может распознать опечатку опираясь на частотность появления слова
            Такой вариант будет работать только в тех случаях, когда процент ошибок очень мал(как в вики статьях)
        """
        if morph.word_is_known(wrd):
            normal_form_wrd = morph.parse(wrd)[0]
            """
                В строчке ниже алгоритм находит все возможные формы слова (если на вход поступает слово, 
                то на выходе получается список из разных форм слова)
                Пример:
                    Вход:
                        раба
                    Выход
                        раба, рыбы, рыбу, рыбам, рыбой и т.д.
                        
                Данный способ получения разных форм слова медленный, но он гарантирует, что в словаре будут все формы.
                Также требуется проанализировать не всю вики, а какую-то часть, так как количесвто новых слов с каждой
                новой статьей все меньше
                
                Альтернативный вариант:
                
                Если брать во внимание факт, что в русской вики около 1 700 000 статей, то можно предположить, что 
                все формы слова можно получить, если до конца проанализировать статьи.  Но это не гарантирует, что 
                в итоге в словаре будут все нужные формы, также этот способ более медленный, чем первый.
            """
            clean_list.extend([normal_form_wrd.lexeme[i].word for i in range(len(normal_form_wrd.lexeme))])
        else:
            continue


def _get_text(data, text):  # Получение текстовой информации из статей вики
    """
        После тестов на скорость скачивания текстов, было решено использовать Wiki API (вместо стандартного парсинга),
        ибо разница по времени выполения одного и того же объема работы была примерно в 2-3 раза

        Поиск статей ведется по названиям
    """
    wikipedia.set_lang("ru")
    for title in data:
        """ 
            Некоторы названия статей могут быть многозначными.
            Пример такого названия: '!'
            В этих случаях Wiki API выдает ошибку, где указано, что для подобных названий нужно уточнение.
            Пример уточнения: '! (восклицательный знак)'
            
            Также стоит отметить, что статьи с такими названиями есть, но текста в них нет (или очень мало). 
            Только ссылки на другие статьи
        """
        try:
            text.append(re.compile('[^а-яА-Я ]').sub('', wikipedia.page(title).content))
            print(title)
        except:
            print("Страница перенаправляет на другие статьи")


def start_auxiliary_threads(data):  # Подключение нескольких потоков, чтобы ускорить процесс получения данных
    clean_list = []

    flow_0 = Thread(target=_clean, args=[data[0:round(len(data)/8)], clean_list])
    flow_1 = Thread(target=_clean, args=[data[round(len(data)/8):round(len(data)/8*2)], clean_list])
    flow_2 = Thread(target=_clean, args=[data[round(len(data)/8*2):round(len(data)/8*3)], clean_list])
    flow_3 = Thread(target=_clean, args=[data[round(len(data)/8*3):round(len(data)/8*4)], clean_list])
    flow_4 = Thread(target=_clean, args=[data[round(len(data)/8*4):round(len(data)/8*5)], clean_list])
    flow_5 = Thread(target=_clean, args=[data[round(len(data)/8*5):round(len(data)/8*6)], clean_list])
    flow_6 = Thread(target=_clean, args=[data[round(len(data)/8*6):round(len(data)/8*7)], clean_list])
    flow_7 = Thread(target=_clean, args=[data[round(len(data)/8*7):len(data)], clean_list])

    flow_0.start()
    flow_1.start()
    flow_2.start()
    flow_3.start()
    flow_4.start()
    flow_5.start()
    flow_6.start()
    flow_7.start()

    flow_0.join()
    flow_1.join()
    flow_2.join()
    flow_3.join()
    flow_4.join()
    flow_5.join()
    flow_6.join()
    flow_7.join()

    return sorted(set(clean_list))


def start_main_threads(data):   # Подключение нескольких потоков, чтобы ускорить процесс получения данных
    text = []

    flow_0 = Thread(target=_get_text, args=[data[0:50], text])
    flow_1 = Thread(target=_get_text, args=[data[50:100], text])
    flow_2 = Thread(target=_get_text, args=[data[100:150], text])
    flow_3 = Thread(target=_get_text, args=[data[150:200], text])
    flow_4 = Thread(target=_get_text, args=[data[200:250], text])
    flow_5 = Thread(target=_get_text, args=[data[250:300], text])
    flow_6 = Thread(target=_get_text, args=[data[300:350], text])
    flow_7 = Thread(target=_get_text, args=[data[350:400], text])

    flow_0.start()
    flow_1.start()
    flow_2.start()
    flow_3.start()
    flow_4.start()
    flow_5.start()
    flow_6.start()
    flow_7.start()


    flow_0.join()
    flow_1.join()
    flow_2.join()
    flow_3.join()
    flow_4.join()
    flow_5.join()
    flow_6.join()
    flow_7.join()

    return text


if __name__ == "__main__":
    with open('data2.csv', newline='', encoding='utf-8') as f:  # Получение данных из предыдущей программы
        reader = csv.reader(f)
        data = list(reader)

    print(tokenizer(start_main_threads(data)))
