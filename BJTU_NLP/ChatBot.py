import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import urllib3
import urllib.request
import re
from bs4 import BeautifulSoup
import pickle
nltk.download('stopwords')
from nltk.corpus import stopwords
import binascii
from nltk.corpus import webtext
from nltk.corpus import nps_chat

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^a-z #+_]')
STOPWORDS = set(stopwords.words('english'))
nltk.download('punkt') # first-time use only
nltk.download('wordnet') # first-time use only

def pre_process(url):
    http = urllib3.PoolManager(retries=False)
    print(url)
    r = http.request('GET', url)
    raw_html = r.data
    soup = BeautifulSoup(raw_html, 'html.parser')
    raw_content = soup.find(id='mw-content-text').find_all('p')
    for idx , elem in enumerate(raw_content):
        raw_content[idx] = elem.text.strip()
    text  = ' '.join(raw_content)
    text = textcleaner(text)
    return (text)

def textcleaner(text):
    text = text.lower()
    text = re.sub(REPLACE_BY_SPACE_RE, " ", text)
    re.sub(BAD_SYMBOLS_RE, "", text)
    tmp = text.split()
    fileredText = []
    for w in tmp:
        if w not in STOPWORDS:
            fileredText.append(w)
    text = ' '.join(fileredText)
    return (text) 

def dl_text():
    f = open ('Url.txt', 'r')
    ListUrl = f.read()
    f.close()
    ListUrl = ListUrl.split("\n")
    ListText = []
    i = 0
    for items in ListUrl:
        ListText.append(pre_process(items))
        i += 1
        print(i)
    Text = ' '.join(ListText)
    with open ('DataSave', 'wb') as out_file:
      pickle.dump(Text, out_file)
    out_file.close()

try:
        with (open("DataSave", "rb")) as openfile:
            raw = pickle.load(openfile)
except:
        dl_text()
        with (open("DataSave", "rb")) as openfile:
            raw = pickle.load(openfile)
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)
lemmer = nltk.stem.WordNetLemmatizer()
   
#WordNet is a semantically-oriented dictionary of English included in NLTK.
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


def run(user_response):
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            return("You are welcome..")
        else:
            if(greeting(user_response)!=None):
                return(greeting(user_response))
            else:
                bite = response(user_response)
                sent_tokens.remove(user_response)
                return(bite)
    else:
        return("Bye! take care..")

#print("Louifion: My name is Louifion. I will answer your queries. If you want to exit, type Bye!")