import numpy
import pandas
from bs4 import BeautifulSoup
import nltk
import requests
import urllib
import re
from sklearn.feature_extraction.text import CountVectorizer
import pickle


list_site = {'http://scrapsfromtheloft.com/2017/05/06/louis-ck-oh-my-god-full-transcript/','https://scrapsfromtheloft.com/2019/09/21/mark-normand-stand-up-tonight-show-starring-jimmy-fallon/', 'https://scrapsfromtheloft.com/2018/09/15/real-time-with-bill-maher-september-14-2018-transcript/', 'https://scrapsfromtheloft.com/2019/04/11/dostoevsky-on-crime-and-punishment-letter-to-m-n-katkov/', 'https://scrapsfromtheloft.com/2018/07/04/roberto-baggio-penalty-miss-1994/'}


nltk.download('stopwords')
from nltk.corpus import stopwords

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))


def get_content(url):
    content = urllib.request.urlopen(url)
    content = BeautifulSoup(content, 'html.parser')
    content = content.findAll('div', attrs={"class": "post-content"})
    new_str = []
    for item in content:
        e = item.findAll('p')
        for i in e:
            new_str.append(i.text)
    return new_str


def text_clear(text):
    text = text.lower()
    text = re.sub(REPLACE_BY_SPACE_RE, " ", text)
    text = re.sub(BAD_SYMBOLS_RE, "", text)
    text = re.sub('[0-9]', '', text)
    text = text.split()
    y = len(text)
    i = 0
    while i < y:
        if text[i] in STOPWORDS:
            del text[i]
            y -= 1
        i += 1
    text = " ".join(text)
    text = re.sub(' +', ' ', text)
    return text


def main():
    y = 0
    final_content = []
    for item in list_site:
        get_all = ""
        content = get_content(item)
        # open a file, where you ant to store the data
        y += 1
        file = open('Data_pickle' + str(y) + '.txt', 'wb')

        # dump information to that file
        pickle.dump(content, file)
        # close the file
        file.close()
        for i in range(len(content)):
            get_all += text_clear(content[i])
        final_content.append(get_all)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(final_content)
    df = pandas.DataFrame(X.toarray())
    result = df.to_csv(index=False, path_or_buf='result.csv', header=vectorizer.get_feature_names())

if __name__ == "__main__":
    main()