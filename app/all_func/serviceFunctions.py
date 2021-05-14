import re
from tqdm import tqdm


def open_file():  # Функция для открытия файла с матерными выражениями
    cores_file = open('app/all_func/swear_words.txt', 'r')
    cores = [line.strip() for line in cores_file.readlines()]
    cores_file.close()
    return cores


def find_word(text, index):  # Поиск слова
    list_of_letters = []
    left_indexes = index - 1
    right_indexes = index

    # Если index находится в середине слова, получаем левую часть слова
    while (left_indexes >= 0 and text[left_indexes].isalpha()):
        list_of_letters.append(text[left_indexes])
        left_indexes -= 1
    list_of_letters_updated = list(reversed(list_of_letters))

    # Получаем правую часть слова
    while (right_indexes <= (len(text) - 1) and text[right_indexes].isalpha()):
        list_of_letters_updated.append(text[right_indexes])
        right_indexes += 1
    word = ''.join(list_of_letters_updated)
    return word


def left_len_of_word(text, index):  # Поиск длины части слова от индекса слева
    list_of_letters = []
    left_indexes = index - 1
    # Если index находится в середине слова, получаем левую часть слова
    while (left_indexes >= 0 and text[left_indexes].isalpha()):
        list_of_letters.append(text[left_indexes])
        left_indexes -= 1
    list_of_letters_updated = list(reversed(list_of_letters))
    left_len = len(list_of_letters_updated)
    return left_len


def get_swear_words(text):  # Получение всех матерных слов в тексте
    swear_words_in_text = []
    swear_list_google = open_file()

    for swear_word in tqdm(swear_list_google):
        result = re.findall(swear_word, text, re.IGNORECASE)  # Находим слова
        if len(result) != 0:
            result = list(dict.fromkeys(result))
            for swear_word in range(len(result)):
                swear_words_in_text.append(
                    result[swear_word])  # Добавляем в лист

    # Получаем лист с уникальными словами
    swear_words_in_text = list(set(swear_words_in_text))
    return swear_words_in_text


def replace_word(text, index_of_entry, left_len, found_word):
    flag = 'z'  # Флаг для замены

    text = text[:(index_of_entry - left_len)] + \
        flag + text[(index_of_entry - left_len) +
                    1:]  # Ставим флаг на слове в тексте

    found_word = found_word[:0] + flag + \
        found_word[0+1:]  # Флаг на найденном слове

    text = text.replace(found_word, len(found_word) *
                        "*", 1)  # Меняем слово в тексте
    return text
