import requests
from bs4 import BeautifulSoup

class Valyrian:

    def __init__(self):
        pass

    def make_url(self, query,mode):
        url='http://www.dictionary.com/browse/'
        if(mode=='thes'):
            url=url.replace('dictionary','thesaurus')
        url += query.strip().lower().replace(' ', '%20')
        return url

    def find_word_data(self, word,mode="dict"):
        url = self.make_url(word, mode)

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        syn=soup.select("div.relevancy-list ul li a span")
        syn=[str(x.text) for x in syn]

        if(mode=='thes'):
            syn=soup.select("div.relevancy-list ul li a span")
            syn=[str(x.text) for x in syn]
            return syn
        meaning_divs= soup.find_all('div', class_="def-content")

        meanings=[str(x.text) for x in meaning_divs]
        meanings=[x.replace('\n','').replace('\r','').strip() for x in meanings]

        return meanings

    def run_data_lookup(self,word):
        meanings=self.find_word_data(word)
        syns=self.find_word_data(word,"thes")
        return {"meanings":meanings,"synonyms":syns}

v=Valyrian()
