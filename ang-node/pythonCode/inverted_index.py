import os
import nltk 
import json
import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from queue import PriorityQueue
import re
import math 
from decimal import Decimal
import regex
import numpy as np
from collections import Counter

#nltk.download('punkt')
#nltk.download('stopwords')

# define N objets
N = 100
tweet1 = dict()
tweets = dict()

class tokenObject:
    def __init__(self):
        self.tf_per_tweet = {} # Term frecuency on text per tweet
        self.df = 0 # Total tweet frecuency
        self.tf = 0 # Total term frecuency

def stopwords_stemmer(filename_tweet_text):
    tokens = nltk.word_tokenize(filename_tweet_text)
    stoplist = stopwords.words("spanish")
    stoplist += ['/…','--','RT','`','@','|','¿','?', '¡', '!','aqui', '.', ',', ';', '«', '»', ':', '(', ')', '"','en', 'En', 'la', 'La', 'con', 'Con','sin', 'Sin', 'al', 'Al', 'de', 'De', 'el', 'El', '#', '$', '^', '&', '*', '%']
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



# def get_frecuency_terms(terms):
#     terms_dict = dict()
#     for term in terms:
#         if term not in terms_dict:
#             terms_dict[term] = 1
#         else:
#             terms_dict[term] += 1
#     return terms_dict

##
#   {   
#       keiko : { 12312312: 3, 421412412, 6},
#       tramposa: {12312312 : 1, 3123124: 5}        
#        
#   }
#  
##

# def readTweets(tweets):
#     term_dict = dict()
#     for tweet in tweets:
#         token_clean = stopwords_stemmer(tweet["text"])
#         id_tweet = tweet["id"] # los id son únicos?
#         terms_with_frequency = Counter(token_clean)
#         for term, freq in terms_with_frequency:
#             if(term not in term_dict):
#                 term_dict[term] = dict()
#                 term_dict[term][id_tweet] = freq
#             else:
#                 term_dict[term][id_tweet] = freq
#     return term_dict


def createVectorTf_idf(tweet):
    vector_tf_idf = np.zeros(N)
    i = 0
    for termId in tweet1.key():
        vector_tf_idf[termId] = tweet1[termId]
    return vector_tf_idf

def parser(query):
    query_clean = stopwords_stemmer(query)
    tf_words_query = Counter(query_clean)
    indice_invertido_dict = open("index_invertido.dat", "r")
    term_termId_dict = open("terms.data", "r")
    result = dict()
    for word, frec in tf_words_query.items():
        if(word in indice_invertido_dict):
            tf = frec
            df = len(indice_invertido_dict[term_termId_dict[word]])
            tf_idf = math.log(1+tf, 10)* math.log(N/df,10)
            result[term_termId_dict[word]] = tf_idf
    return result
    
def cosine(q, doc):
    return np.dot(q,doc)/(np.linalg.norm(q)* np.linalg.norm(doc))

# Nos trae los (id, cosine_value) menor a mayor. Menor distancia mayor 
def searchKNN(query, k):
    pq = PriorityQueue()
    v_query = createVectorTf_idf(parser(query))
    for id, value in tweets.items():
        v = createVectorTf_idf(value)
        valor = cosine(v_query, v)
        pq.put((valor, id))
    result = []
    while pq.empty()!= 1:
        data = pq.get()
        result.append(data)
    return result[:k]


def retrieve_tweet(docId):
    json_path = './data/'
    tweets = os.listdir(json_path)
    with open(json_path + tweets[0], encoding="utf8") as file:
        json_content = json.load(file)
        for json_str in json_content:
            id = str(json_str['id'])
            if id == docId:
                return json.dumps(json_str) 
                


def retrieve_tweets(query,k):
    res = []
    distances = searchKNN(query,k)
    for tuples in distances:
        distance = tuples[0]
        docId = tuples[1]   # tweetId
        res.append(json.loads(retrieve_tweet(docId)))
    return json.dumps(res)

result_data = retrieve_tweets(str(sys.argv[1]),9)
result_data = json.loads(result_data)
with open('result_db.json', 'w') as file:
    json.dump(result_data, file)