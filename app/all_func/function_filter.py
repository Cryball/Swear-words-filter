from tqdm import tqdm
from fuzzywuzzy import fuzz
import gensim
import difflib
import re
import logging
from serviceFunctions import find_word, left_len_of_word, get_swear_words, replace_word
import app_logger

w2v_test = gensim.models.Word2Vec.load("app/word2vecmodel/word2vec.model")
words_test_w2v = list(w2v_test.wv.key_to_index)

logger = app_logger.get_logger(__name__)


def filter(text):
    logger.info("Программа стартует")
    # Главная функция
    # Получаем лист всех матерных слов в тексте
    list_swear_words_in_text = get_swear_words(text)
    logger.info("Список запрещенных слов в тексте")
    print(list_swear_words_in_text)
    logger.info("Происходит замена слов")
    for word in tqdm(range(0, len(list_swear_words_in_text))):
        going_to_next_index = 0
        swear_word = list_swear_words_in_text[word]

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
