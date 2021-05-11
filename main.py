import pandas as pd
import numpy as np
from tqdm import tqdm
import pickle
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import re
import gensim
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from gensim.test.utils import common_corpus, common_texts, get_tmpfile
import nltk
from nltk.tokenize import sent_tokenize, RegexpTokenizer, word_tokenize
from nltk.corpus import stopwords
from gensim.test.utils import common_texts
import logging

from flask import Flask, request

w2v_test = gensim.models.Word2Vec.load("word2vec.model")
words_test = list(w2v_test.wv.key_to_index)


def open_file():  # Функция для открытия файла с матерными выражениями
    cores_file = open('swear_words.txt', 'r')
    cores = [line.strip() for line in cores_file.readlines()]
    cores_file.close()
    return cores


def def_word(text, ind):  # Поиск слова
    raw = []
    x = ind - 1
    y = ind
    while (x >= 0 and text[x].isalpha() == True):
        raw.append(text[x])
        x -= 1
    raw1 = list(reversed(raw))
    imp_val = len(raw1)

    while (y <= (len(text) - 1) and text[y].isalpha() == True):
        raw1.append(text[y])
        y += 1
    word = ''.join(raw1)
    return word


def right_len(text, ind):  # Поиск длины найденного слова от индекса справа
    raw = []
    x = ind - 1
    y = ind
    while (x >= 0 and text[x].isalpha() == True):
        raw.append(text[x])
        x -= 1
    raw1 = list(reversed(raw))
    imp_val = len(raw1)
    return imp_val


def filter(text):  # Главная функция
    b = []
    #text = text.lower()
    swear_list = open_file()
    for i in tqdm(swear_list):
        res1 = re.findall(i, text, re.IGNORECASE)
        #res2 = re.findall(i.upper(), text, re.IGNORECASE)
        # print(res2)

        if len(res1) != 0:
            res1 = list(dict.fromkeys(res1))
            for i in range(len(res1)):
                b.append(res1[i])
            #res1 = ' '.join(res1)
            # b.append(res1)

        # if len(res2) != 0:
        #     res2 = list(dict.fromkeys(res2))
        #     res2 = ' '.join(res2)
        #     b.append(res2)
    b = list(set(b))
    print(b)

    for j in tqdm(range(0, len(b))):
        m = 0
        if b[j] in words_test:
            #print(b[j] + "_word in dict")
            while b[j] in text:
                log = text.find(b[j], m)
                m = log + 1
                if log == -1:
                    break
                x = def_word(text, log)
                #print(x + "_found")
                imp_val = right_len(text, log)
                y = b[j]
                if x in words_test:

                    if (w2v_test.wv.similarity(x, y)) > 0.6:
                        # print('lol')
                        new_character = 'z'
                        text = text[:(log - imp_val)] + \
                            new_character + text[(log - imp_val)+1:]
                        x = x[:0] + new_character + x[0+1:]
                        x = x.replace(x[0], "z", 1)
                        text = text.replace(x, len(x)*"*", 1)

                else:
                    if fuzz.token_sort_ratio(x, y) >= 60:
                        new_character = 'z'
                        text = text[:(log - imp_val)] + \
                            new_character + text[(log - imp_val)+1:]
                        x = x[:0] + new_character + x[0+1:]
                        text = text.replace(x, len(x)*"*", 1)

        else:
            while b[j] in text:
                log = text.find(b[j], m)
                # print(log)
                m = log + 1
                if log == -1:
                    break
                x = def_word(text, log)
                imp_val = right_len(text, log)
                y = b[j]
                if fuzz.token_sort_ratio(x, y) >= 60:
                    new_character = 'z'
                    text = text[:(log - imp_val)] + \
                        new_character + text[(log - imp_val)+1:]
                    x = x[:0] + new_character + x[0+1:]
                    text = text.replace(x, len(x)*"*", 1)

    b.clear()
    return text


#text = "Ass fUck i love u fuck bullshit LOVE NO PoIson piece of shit BITCH fUcK YOU ASS aNAl"
#print(filter(text))


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        text = request.form.get('text')
        result = filter(text)
        return ''' Готовый текст: {}'''.format(result)

    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Введите текст для фильтрации: <input type="text" name="text"></label></div>
               <input type="submit" value="Submit">
           </form>'''


if __name__ == '__main__':
    Flask.run(app, port=5000, host = "0.0.0.0")
