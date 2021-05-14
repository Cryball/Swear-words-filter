from tqdm import tqdm
from fuzzywuzzy import fuzz
import re
import gensim
from flask import Flask, request
from serviceFunctions import find_word, left_len_of_word, get_swear_words, replace_word

w2v_test = gensim.models.Word2Vec.load("app/word2vecmodel/word2vec.model")
words_test_w2v = list(w2v_test.wv.key_to_index)


def filter(text):  # Главная функция
    # Получаем лист всех матерных слов в тексте
    list_swear_words_in_text = get_swear_words(text)
    print(list_swear_words_in_text)
    for j in tqdm(range(0, len(list_swear_words_in_text))):
        going_to_next_index = 0
        swear_word = list_swear_words_in_text[j]

        while swear_word in text:

            # Получаем индекс первой буквы матерного слова в тексте
            index_of_entry = text.find(swear_word, going_to_next_index)
            # Переменная для перехода к следующему индексу
            going_to_next_index = index_of_entry + 1

            if index_of_entry == -1:
                break

            # Находим слово, в котором включено матерное слово
            found_word = find_word(text, index_of_entry)
            left_len = left_len_of_word(text, index_of_entry)
            # Если матерное и найденное слово в модели, то используем проверку с моделью
            if (found_word in words_test_w2v) and (swear_word in words_test_w2v):
                if (w2v_test.wv.similarity(found_word, swear_word)) > 0.6:
                    text = replace_word(
                        text, index_of_entry, left_len, found_word)

            else:  # Если матерное или найденное слово не в модели, то делаем проверку расстоянием Левенштейна
                if fuzz.token_sort_ratio(found_word, swear_word) >= 80:
                    text = replace_word(
                        text, index_of_entry, left_len, found_word)

    list_swear_words_in_text.clear()
    return text


#text = "Ass fUck i love u fuck bullshit LOVE NO PoIson piece of shit BITCH fUcK YOU ASS aNAl"
#text = "FUCK fUck UCK FUCK ass BiTch Asshole ass hole in butt anal pass grass class classic anal Anal ANALYZE AnAlYzE"
# print(filter(text))


# Далее код для WebApi
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form_example():

    if request.method == 'POST':
        text = request.form.get('text')
        result = filter(text)
        return ''' Готовый текст: {}'''.format(result)

    return '''
           <form method="POST">
               <div><label>Введите текст для фильтрации: <input type="text" name="text"></label></div>
               <input type="submit" value="Submit">
           </form>'''


if __name__ == '__main__':
    Flask.run(app, port=5000, host="0.0.0.0")
