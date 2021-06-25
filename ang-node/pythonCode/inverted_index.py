import os
import nltk 
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from queue import PriorityQueue
import re
import math 
from decimal import Decimal
import regex

#nltk.download('punkt')
#nltk.download('stopwords')

def stopwords_stemmer(filename_tweet_text):
    tokens = nltk.word_tokenize(filename_tweet_text)
    stoplist = stopwords.words("spanish")
    stoplist += ['`','@','|','¿','?', '¡', '!','aqui', '.', ',', ';', '«', '»', ':', '(', ')', '"','en', 'En', 'la', 'La', 'con', 'Con','sin', 'Sin', 'al', 'Al', 'de', 'De', 'el', 'El', '#', '$', '^', '&', '*', '%']
    tokens_clean = tokens.copy()

    for token in tokens:
        if token in stoplist:
            tokens_clean.remove(token)
            
    stemmer = SnowballStemmer("spanish")
    for token in tokens_clean:
        token = stemmer.stem(token)

    return tokens_clean

json_path = './data/'
tweets = os.listdir(json_path)
with open(json_path + tweets[0], encoding="utf8") as file:
    json_content = json.load(file)
    for content in json_content:
        tokens_clean = stopwords_stemmer(content["text"])
        print(tokens_clean, '\n')
