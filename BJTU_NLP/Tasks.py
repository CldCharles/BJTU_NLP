import urllib.request
import re
from bs4 import BeautifulSoup
import pickle
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd

ListUrl = ["http://scrapsfromtheloft.com/2017/05/06/louis-ck-oh-my-god-full-transcript/", "https://scrapsfromtheloft.com/2019/10/13/khomeinis-iran/", "https://scrapsfromtheloft.com/2019/04/11/dostoevsky-on-crime-and-punishment-letter-to-m-n-katkov/", "https://scrapsfromtheloft.com/2017/12/01/tom-petty-running-down-a-dream/", "https://scrapsfromtheloft.com/2019/07/07/yuval-noah-harari-talks-at-google-transcript/"]
listPage = []
for i in ListUrl:
    listPage.append(urllib.request.urlopen(i).read())

soup = []
for i in listPage:
    soup.append(BeautifulSoup(i, 'html.parser'))

SoupTab = []
for i in soup:
    tmp = i.find('div',attrs={"class":"post-content"}).find_all("p")
    for cpt, elem in enumerate(tmp):
        tmp[cpt] = elem.text
    SoupTab.append(" ".join(tmp))


with open ('transcripts', 'wb') as out_file:
    pickle.dump(SoupTab, out_file)
out_file.close()

for i in range(0, len(SoupTab)): 
    SoupTab[i] = SoupTab[i].lower()

CleanedText = []

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^a-z #+_]')
STOPWORDS = set(stopwords.words('english'))
NewList = []

for i in range(0, len(SoupTab)):
    SoupTab[i] = re.sub(REPLACE_BY_SPACE_RE, "", SoupTab[i])

for i in range(0, len(SoupTab)):
    SoupTab[i] = re.sub(BAD_SYMBOLS_RE, "", SoupTab[i])

Text = []  
for items in SoupTab:
    if items not in STOPWORDS:
        Text.append(items)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(Text).toarray()
print(vectorizer.get_feature_names())
print(X)

frame = pd.DataFrame(X)
frame.columns = vectorizer.get_feature_names()

frame.to_csv(index='false', path_or_buf="Output.csv", sep=";")
