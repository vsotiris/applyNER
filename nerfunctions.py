from bs4 import BeautifulSoup
import collections
from GoogleNews import GoogleNews
import pandas as pd
import requests
import spacy
nlp = spacy.load("en_core_web_sm")

def getgooglenews(keywords, period):
    language = 'en'
    print(keywords)
    googlenews = GoogleNews(period=period)
    googlenews.search(keywords)
    for i in range(2, 3):
        googlenews.getpage(i)
        result = googlenews.result()
        df = pd.DataFrame(result)

    newsdata = df.drop(columns=["img"])
    return newsdata

def geturls(newsdf, numarticles):
    URL = []
    for i in range(0, numarticles):
        URL.append(newsdf['link'][i])
    print(len(URL))
    return URL

def getorg(doc):  # NER
    doc = nlp(doc)
    orgs = []
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            orgs.append(ent.text)
    orgfreq = collections.Counter(orgs)
    orgsortedfreq = sorted(orgfreq.items(), key=lambda item: item[1], reverse=True)
    return orgsortedfreq

def createdoc(URL, numwords):
    ARTICLES = []  # list of articles
    for url in URL:
        ARTICLE = geturltext(numwords, url)
        ARTICLES.append(ARTICLE)
    doc = ''.join(ARTICLES)
    return doc

# extract and inspect the first N words in the first article
def geturltext(numwords, url):
    r = requests.get(url)  # grab the web page
    soup = BeautifulSoup(r.text, 'html.parser')
    paragraphs = soup.find_all('p')  # find all paragraphs
    text = [paragraph.text for paragraph in paragraphs]
    words = ' '.join(text).split(' ')[:numwords]
    a = ' '.join(words)[:numwords]
    return a

def find_entities(keywords, timeperiod):
    numarticles = 5
    maxwords = 2000
    newsdata = getgooglenews(keywords, timeperiod)
    print('*** got google news data')
    urlsearch = geturls(newsdata, numarticles)
    searchdoc = createdoc(urlsearch, maxwords)
    results = getorg(searchdoc)
    return results
