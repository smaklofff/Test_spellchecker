import csv
import re
from spellchecker import SpellChecker
import re
from collections import Counter
from symspellpy import SymSpell, Verbosity
import pandas as pd


def _csv_writer(data, path):    # Записывает данные в csv файл (нужно использовать только 1 раз для загрузки файла)
    frame = pd.DataFrame(data)
    frame.to_csv(path, index=False, sep=' ')


def pyspellchecker(sentence):
    misspelled = spell.unknown(re.split(r'\W+', sentence))
    correct_word_list = []
    wrong_word_list = []
    for word in misspelled:
        wrong_word_list.append(word)
        correct_word_list.append(spell.correction(word))
    return f'\nВаше предложение: {sentence}\n' \
           f'Опечатка в словах: {wrong_word_list}\n' \
           f'Наиболее вероятная правильная форма: {correct_word_list}'


def symspell(sentence):
    suggestions = sym_spell.lookup_compound(sentence,
                                            max_edit_distance=2,
                                            transfer_casing=True)
    return f'\n\nВаш предложение: {sentence}\n' \
           f'Наиболее вероятная правильная форма: {suggestions[0]}'



def words(text):
    return re.findall(r'\w+', text[:round(len(text)/10)].lower()) + \
           re.findall(r'\w+', text[round(len(text)/10):round(len(text)*2/10)].lower()) +\
           re.findall(r'\w+', text[round(len(text)*2/10):round(len(text)*3/10)].lower()) + \
           re.findall(r'\w+', text[round(len(text)*3/10):round(len(text)*4/10)].lower()) + \
           re.findall(r'\w+', text[round(len(text)*4/10):round(len(text)*5/10)].lower()) + \
           re.findall(r'\w+', text[round(len(text)*5/10):round(len(text)*6/10)].lower()) + \
           re.findall(r'\w+', text[round(len(text)*6/10):round(len(text)*7/10)].lower()) + \
           re.findall(r'\w+', text[round(len(text)*7/10):round(len(text)*8/10)].lower()) + \
           re.findall(r'\w+', text[round(len(text)*8/10):round(len(text)*9/10)].lower())


if __name__ == "__main__":

    WORDS = Counter(words(open('Standart_text.txt',
                               newline='',
                               encoding='utf-8').read()))
    print("Идет подготовка данных...")

    spell = SpellChecker()
    spell._word_frequency.load_text_file('data.csv')

    array = WORDS.items()   # Нужно использовать только 1 раз
    _csv_writer(WORDS.items(),
                Path(Path.home(), 'AppData', 'Roaming', 'Python', 'Python38', 'site-packages', 'symspellpy', 'Symtext.txt')) # Нужно использовать только 1 раз

    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    sym_spell.load_dictionary(
        Path(Path.home(), 'AppData', 'Roaming', 'Python', 'Python38', 'site-packages', 'symspellpy', 'Symtext.txt'),
        term_index=0,
        count_index=1,
        encoding='utf-8')

    sentence = input('Введите предложение:')

    print(pyspellchecker(sentence))

    print(symspell(sentence))
