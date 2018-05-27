import requests, shelve, random
from bs4 import BeautifulSoup
from Elements import *
import shelve

class Valyrian:

    def __init__(self, citidel):
        self.__citidel=citidel
        shelf=self.get_shelf()
        self.__data=shelf.get('words',[])
        self.define_data()
        shelf.close()
        self.clean()
        print ('Language Discovered')

    def get_shelf(self):
        try:
            shelf=shelve.open(self.__citidel.consts['vocab_path'],writeback=True)
        except:
            shelf=shelve.open('vocab',writeback=True)
        return shelf

    def clean(self):
        shelf=self.get_shelf()
        language_data=shelf.get('words',[])
        language_data=[word for word in language_data if not word.needed_code%2]
        shelf['words']=language_data
        self.__data=language_data
        for i in range(100):
            trgt=random.choice(self.__data)
            if(trgt.needed_code>0):
                try:
                    self.refresh_word(trgt.word)
                except:
                    pass
        self.define_data()
        shelf.close()

    def refresh_word(self,word):
        syns, sents = self.find_word_data(word, 'thes')
        word=self.__data[self.__vocab.index(word)]
        if(word.needed_code>3):
            word.sentences=sents[:3]
        if(word.needed_code>1):
            word.synonyms=syns[:8]

    def define_data(self):
        self.__vocab=[x.word for x in self.__data]
        self.__lang_complexity=[x.complexity for x in self.__data]

    def have_this_in_mind(self,word):
        word=[x for x in self.__data if x.word==word][0]
        self.is_irrelevent(word, 25)

    def get_word(self, word):
        if (word not in self.__vocab):
            word_data=self.run_data_lookup(word)
            word=Word(word,word_data)
            self.add_to_shelf([word])
        else:
            word=self.__data[self.__vocab.index(word)]
        if(not word.complexity):
            self.is_relevent(word)
        return word

    def init_test(self):
        self.__tested=[]
        num_words=len([x for x in self.__lang_complexity if x])
        for case in range(min((5, num_words))):
            word=self.get_test_word()
            while((word.word in [x[0] for x in self.__tested])):
                word=self.get_test_word()
            self.__tested+=[(word.word,random.choice(word.meanings))]
        self.__test_wrongs=[random.choice(word.meanings) for word in self.__data if word.word not in [x[0] for x in self.__tested]]
        return self.__tested

    def get_options(self, right):
        options=random.sample(self.__test_wrongs,3)+[right]
        random.shuffle(options)
        return options

    def get_test_word(self):
        rand_key,i=random.randint(0,sum(self.__lang_complexity)),0
        while(rand_key>self.__lang_complexity[i]):
            rand_key-=self.__lang_complexity[i]
            i+=1
        return self.__data[i]

    def mark_as_irrelevent(self,word):
        word=[x for x in self.__data if x.word==word][0]
        self.is_irrelevent(word)

    def is_irrelevent(self, word, lim=301):
        for _ in range(lim):
            word.occured()
        self.commit_lang_changes()

    def is_relevent(self, word):
        word.new_memory()
        self.commit_lang_changes()

    def commit_lang_changes(self):
        shelf=self.get_shelf()
        shelf['words']=self.__data
        self.define_data()
        shelf.close()

    def add_literature(self,text):
        data=strip_search(text,self.__data)
        new_found=[self.get_word(word) if (word not in self.__vocab) else self.__data[self.__vocab.index(word)].occured() for word in data]
        self.add_to_shelf(new_found)

    def add_to_shelf(self,column):
        self.__data+=[x for x in column if x]
        self.__vocab+=[x.word for x in column if x]
        self.__lang_complexity+=[x.complexity for x in column if x]
        shelf=self.get_shelf()
        shelf['words']=self.__data
        shelf.close()


    def make_word_data_url(self, query,mode):
        url='http://www.dictionary.com/browse/'+query.strip().lower().replace(' ', '%20')
        if(mode=='thes'):
            return url.replace('dictionary','thesaurus')
        return url

    def find_word_data(self, word,mode="dict"):
        r = requests.get(self.make_word_data_url(word, mode))
        soup = BeautifulSoup(r.content, 'html.parser')

        if(mode=='thes'):
            syn=soup.select("a.css-ebz9vl")+soup.select("a.css-vdoou0")
            syn=[x.text.encode('utf-8') for x in syn]
            sents=(soup.select("div.ek2vqzh1")[1:])
            sents=[x.text.encode('utf-8') for x in sents[0].children]
            return syn, sents

        meaning_divs= soup.select("span.e10vl5dg6")
        meanings=[x.text.encode('utf-8') for x in meaning_divs]
        meanings=[x.replace('\n','').replace('\r','').strip() for x in meanings]
        return meanings

    def run_data_lookup(self,word):
        try:
            syns,sents=self.find_word_data(word,"thes")
        except:
            syns,sents=[],[]
        return {"meanings":self.find_word_data(word),"synonyms":syns,"sentences":sents}
