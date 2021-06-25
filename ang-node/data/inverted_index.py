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

nltk.download('punkt')
nltk.download('stopwords')

def stopwords_stemmer(filename_tweet_text):
    file_content = open(filename_tweet_text).read()
    tokens = nltk.word_tokenize(file_content)
    stoplist = stopwords.words("spanish")
    stoplist += ['|','¿','?', '¡', '!','aqui', '.', ',', ';', '«', '»', ':', '(', ')', '"','en', 'En', 'la', 'La', 'con', 'Con','sin', 'Sin', 'al', 'Al', 'de', 'De', 'el', 'El', '#', '$', '^', '&', '*', '%']
    tokens_clean = tokens.copy()

    for token in tokens:
        if token in stoplist:
            tokens_clean.remove(token)

    stemmer = SnowballStemmer("spanish")
    for token in tokens_clean:
        token = stemmer.stem(token)
