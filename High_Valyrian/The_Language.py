import requests
from bs4 import BeautifulSoup

class Valyrian:

    def __init__(self):
        print ('Language Found')
        pass

    def make_word_data_url(self, query,mode):
        url='http://www.dictionary.com/browse/'
        if(mode=='thes'):
            url=url.replace('dictionary','thesaurus')
        url += query.strip().lower().replace(' ', '%20')
        return url

    def find_word_data(self, word,mode="dict"):
        url = self.make_word_data_url(word, mode)

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        syn=soup.select("div.relevancy-list ul li a span")
        syn=[str(x.text) for x in syn]

        if(mode=='thes'):
            syn=soup.select("div.relevancy-list ul li a span")
            syn=[str(x.text) for x in syn]

            sents=(soup.select("div#example-sentences p"))
            sents=[sen for sen in sents]
            data=[y.text.replace('\n','').strip() for y in sents]
            sents=[x.encode('utf-8') for x in data]
            return syn, sents
        meaning_divs= soup.find_all('div', class_="def-content")

        meanings=[str(x.text) for x in meaning_divs]
        meanings=[x.replace('\n','').replace('\r','').strip() for x in meanings]

        return meanings

    def run_data_lookup(self,word):
        meanings=self.find_word_data(word)
        syns,sents=self.find_word_data(word,"thes")
        return {"meanings":meanings,"synonyms":syns,"sentences":sents}
    
