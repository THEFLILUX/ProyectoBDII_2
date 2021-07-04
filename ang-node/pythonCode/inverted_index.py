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
import pickle

bin_path = './bin/'

term_termid_dict_file = open(bin_path + "term_termid_dict.dat", "rb")
tweet_termids_dict_file = open(bin_path + "tweet_termids_dict.dat", "rb")
filenameid_filename_dict_file = open(bin_path + "filenameid_filename_dict.dat", "rb")
termid_df_dict_file = open(bin_path + "termid_df_dict.dat", "rb")
N_file = open(bin_path + "N.dat", "rb")
NTerms_file = open(bin_path + "NTerms.dat", "rb")

#nltk.download('punkt')
#nltk.download('stopwords')

# define N objets
N = pickle.load(N_file)
NTerms = pickle.load(NTerms_file)
termid_df_dict = pickle.load(termid_df_dict_file)
tweet_termids_dict = pickle.load(tweet_termids_dict_file)
term_termid_dict = pickle.load(term_termid_dict_file)
filenameid_filename_dict = pickle.load(filenameid_filename_dict_file)

def stopwords_stemmer(tweet_text):
    tokens = nltk.word_tokenize(tweet_text)
    stoplist = stopwords.words("spanish")
    stoplist += ['/…','--','RT','`','@','|','¿','?', '¡', '!','aqui', '.', ',', ';', '«', '»', ':', '(', ')', '"','en', 'En', 'la', 'La', 'con', 'Con','sin', 'Sin', 'al', 'Al', 'de', 'De', 'el', 'El', '#', '$', '^', '&', '*', '%']
    tokens_clean = tokens.copy()

    for token in tokens:
        if token in stoplist:
            tokens_clean.remove(token)
            
    stemmer = SnowballStemmer("spanish")
    for i in range(len(tokens_clean)):
        tokens_clean[i] = stemmer.stem(tokens_clean[i])

    return tokens_clean


def createVectorTF_IDF(tweet):
    vector_tf_idf = np.zeros(NTerms)
    for term_id in tweet:
        vector_tf_idf[term_id] = tweet[term_id]
    return vector_tf_idf

def parser(query):
    query_clean = stopwords_stemmer(query)
    each_term_frequency = Counter(query_clean)
    result = {}
    for term in each_term_frequency:
        if(term in term_termid_dict):
            term_id = term_termid_dict[term]
            tf = each_term_frequency[term]
            df = termid_df_dict[term_id]
            tf_idf = math.log(1 + tf, 10)* math.log(N/df,10)
            result[term_id] = tf_idf
    return result
    
def cosine(q, doc):
    r = np.dot(q,doc)/(np.linalg.norm(q) * np.linalg.norm(doc))
    #if(r > 0):
    #    print(r)
    return r
# Nos trae los (id, cosine_value) menor a mayor. Menor distancia mayor 
def searchKNN(query, k):
    pq = PriorityQueue()
    v_query = createVectorTF_IDF(parser(query))
    for tweet_id in tweet_termids_dict:
        v = createVectorTF_IDF(tweet_termids_dict[tweet_id][1])
        valor = cosine(v_query, v)
        if(pq.qsize() < k):
            pq.put((valor, tweet_id))
        else:
            top = pq.get()
            if(valor > top[0]):
                pq.put((valor, tweet_id))
            else:
                pq.put(top)
    result = [0] * k
    i = k - 1
    while not pq.empty():
        data = pq.get()
        result[i] = data
        i -= 1
    return result


def retrieve_tweet(docId):
    json_path = './data2/'
    filenameid = tweet_termids_dict[docId][0]
    filename = filenameid_filename_dict[filenameid]
    with open(json_path + filename, encoding="utf8") as file:
        json_content = json.load(file)
        for tweet in json_content:
            if tweet['id'] == docId:
                return json.dumps(tweet) 

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