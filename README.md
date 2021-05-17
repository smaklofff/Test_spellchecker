# Spellchecker
**Spellchecker** - это программа, осуществляющая проверку заданного текста на наличие в нём орфографических ошибок.  
В "Test_spellckecker" реализован не только сам spellchecker, но и сбор и обработка данных, которые будет использовать алгоритм.
## Description
Задача:
- Скачать все тексты всех статей русскоязычной википедии
- Сохранить все уникальные словоформы всех слов ( т.е. рыба, рыбы, рыбу, рыбам, рыбой и т.д. ) в словарь.   
- При проверке орфографии, считать слово ошибочным, если оно не присутствует в словаре

Для каждого пункта из задания была создана собственная программа. Это сделано для того, чтобы упростить тестирование.
Список файлов с кодом:
1. Parser_1
2. Parser_2
3. Spellchecker

### Parser_1
Программа в этом файле собрает названия статей. Это нужно, чтобы Wiki API смогла найти статьи по названиям. Подробнее про работу Wiki API будет расказано во втором разделе.  
А теперь к главной части программы:
```
def _main(link):  # Переходит на страницы, где есть названия статей
    while len(href_list) < 100000:
        response = requests.get(link)
        link = 'https://ru.wikipedia.org/'
        soup = BeautifulSoup(response.text, 'lxml')
        block = soup.find('ul', class_='mw-allpages-chunk')
        _link_list(block)
        link = urljoin(link, soup.find('div', class_='mw-allpages-nav').contents[-1].attrs['href'])
```
На вход этой функции поступает ссылка на страницу, где находятся все статьи русской вики. В теле функции расположен стандартный парсер, где  ***block*** - контейнер (div), в котором находятся все названия, ***_link_list()*** - дополнительная функция, которая получает названия и ***link*** - ссылка на другую страницу с названиями.  

После выполнения этой программы в csv файл будут записаны все названия русских статей.  
Примерная скорость работы - 250 названий в секунду

### Parser_2

Вторая часть программы получает тексты всех статей и обрабатывает их. На выходе получается 2 файла: "грязный" текст и словарь из слов, которые встречались.
Рассмотрим функцию:
```
def _clean(data, clean_list):   # Очищает полученные данные
    morph = pymorphy2.MorphAnalyzer()
    for wrd in data:
        if morph.word_is_known(wrd):
            normal_form_wrd = morph.parse(wrd)[0]
            clean_list.extend([normal_form_wrd.lexeme[i].word for i in range(len(normal_form_wrd.lexeme))])
```
В строчке ``` if morph.word_is_known(wrd): ``` происходит проверка на существование слова. Это нужно, чтобы поймать опечатки и слова, которых нет. После проверки в словарь сохраняются все уникальные словоформы.








