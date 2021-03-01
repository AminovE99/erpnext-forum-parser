import nltk
import xmltodict
import re

from nltk.corpus import stopwords
from pymystem3 import Mystem
from nltk.stem import WordNetLemmatizer


def is_good_word(word):
    match = re.match("""^[a-zA-Z]+$""", word)
    return bool(match)


def normilize(word):
    if '\n' in word:
        word = word[:-2]
    return word.lower()


def return_list_of_words(text):
    list_with_raw_words = text.split(' ')
    list_with_words = list(map(normilize, list(filter(lambda x: is_good_word(x), list_with_raw_words))))
    list_without_stop_words = list(filter(lambda x: x not in set(stopwords.words('english')), list_with_words))
    return list_without_stop_words


if __name__ == '__main__':
    nltk.download('stopwords')
    lemmas = ''
    m = Mystem()
    with open('xml_result.xml', 'r') as file:
        xml = file.read()
        xml = xmltodict.parse(xml)

    list_with_doc = xml['documents']['document']
    lemmatizer = WordNetLemmatizer()
    nltk.download('wordnet')
    for doc in xml['documents']['document']:
        if doc['text'] is not None:
            list_of_words = return_list_of_words(doc['text'])
            print(list_of_words)
            list_of_lemmatized_words = list(map(lambda x: lemmatizer.lemmatize(x), list_of_words))
            print(list_of_lemmatized_words)
            with open('output.txt', 'a') as file:
                file.write(str(list_of_lemmatized_words) + "\n")
