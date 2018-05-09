import requests, shelve
from bs4 import BeautifulSoup
from Elements import *
import shelve

class Valyrian:

    def __init__(self, citidel):
        self.__citidel=citidel
        shelf=shelve.open(self.__citidel.consts['vocab_path'],writeback=True)
        self.__data=shelf.get('words',[])
        self.__vocab=[x.word for x in self.__data]
        shelf.close()
        print ('Language Discovered')
        self.clean()

    def clean(self):
        # TODO handle 0<needed_code<7
        shelf=shelve.open(self.__citidel.consts['vocab_path'],writeback=True)
        language_data=shelf.get('words',[])
        language_data=[word for word in language_data if word.needed_code<7]
        shelf['words']=language_data
        self.__data=language_data
        self.__vocab=[x.word for x in self.__data]
        shelf.close()

    def get_word(self, word):
        if (word not in self.__vocab):
            word_data=self.run_data_lookup(word)
            word=Word(word,word_data)
            self.add_to_shelf([word])
            return word
        return self.__data[self.__vocab.index(word)]

    def add_literature(self,text):
        data=strip_search(text,self.__data)
        new_found=[self.get_word(word) if (word not in self.__vocab) else self.__data[self.__vocab.index(word)].occured() for word in data]
        self.add_to_shelf(new_found)

    def add_to_shelf(self,column):
        self.__data+=[x for x in column if x]
        self.__vocab+=[x.word for x in column if x]
        shelf=shelve.open(self.__citidel.consts['vocab_path'],writeback=True)
        shelf['words']=self.__data
        shelf.close()


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

        if(mode=='thes'):
            syn=soup.select("a.css-wf816l")
            syn=[x.text.encode('utf-8') for x in syn]
            more_syn=soup.select("a.css-1iq9guo")
            syn+=[x.text.encode('utf-8') for x in more_syn]
            sents=(soup.select("div.ek2vqzh1")[1:])
            sents=[x.text.encode('utf-8') for x in sents[0].children]
            
    ##        sents=[sen for sen in sents]
    ##        data=[y.text.replace('\n','').strip() for y in sents]
    ##        sents=[x.encode('utf-8') for x in data]
            return syn, sents
        meaning_divs= soup.find_all('div', class_="def-content")

        meanings=[x.text.encode('utf-8') for x in meaning_divs]
        meanings=[x.replace('\n','').replace('\r','').strip() for x in meanings]

        return meanings

    def run_data_lookup(self,word):
        meanings=self.find_word_data(word)
        syns,sents=self.find_word_data(word,"thes")
        return {"meanings":meanings,"synonyms":syns,"sentences":sents}
