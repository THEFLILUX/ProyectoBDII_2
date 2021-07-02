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

class tokenObject:
    def __init__(self):
        self.tf_per_tweet = {} # Term frecuency on text per tweet
        self.df = 0 # Total tweet frecuency
        self.tf = 0 # Total term frecuency

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
inverted_index={}
with open(json_path + tweets[0], encoding="utf8") as file:
    json_content = json.load(file)
    for tweet in json_content:
        tokens_clean = stopwords_stemmer(tweet["text"])
        for token in tokens_clean:
            if token not in inverted_index:
                inverted_index[token] = tokenObject()
                inverted_index[token].tf += 1
                if tweet["id"] not in inverted_index[token].tf_per_tweet:
                    inverted_index[token].tf_per_tweet[tweet["id"]] = 1
                    inverted_index[token].df += 1
                else:
                    inverted_index[token].tf_per_tweet[tweet["id"]] += 1



def get_frecuency_terms(terms):
    terms_dict = dict()
    for term in terms:
        if term not in terms_dict:
            terms_dict[term] = 1
        else:
            terms_dict[term] += 1
    return terms_dict

##
#   {   
#       keiko : { 12312312: 3, 421412412, 6},
#       tramposa: {12312312 : 1, 3123124: 5}        
#        
#   }
#  
##

def readTweets(tweets):
    term_dict = dict()
    for tweet in tweets:
        token_clean = stopwords_stemmer(tweet["text"])
        id_tweet = tweet["id"] # los id son únicos?
        terms_with_frequency = get_frecuency_terms(token_clean)
        for term, freq in terms_with_frequency:
            if(term not in term_dict):
                term_dict[term] = dict()
                term_dict[term][id_tweet] = freq
            else:
                term_dict[term][id_tweet] = freq
    return term_dict

# versión 2
# Using variable global

