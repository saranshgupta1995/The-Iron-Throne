from Utils import *

class Word:

    def __init__(self,word, word_data):
         self.__word=word
         self.__meanings=word_data.get('meanings',[])
         self.__synonyms=word_data.get('synonyms',[])
         self.__sentences=word_data.get('sentences',[])
         self.__length=len(word)
         self.__occurances=0
         self.__complexity=100

    @property
    def meanings(self):
        return self.__meanings

    @property
    def synonyms(self):
        return self.__synonyms

    @property
    def sentences(self):
        return self.__sentences

    @property
    def word(self):
        return self.__word

    @property
    def length(self):
        return self.__length

    def __str__(self):
        return self.word

class Sentence:

    def __init__(self, sentence):
        self.__sentence=sentence
        self.__stripped_sen=strip_search(sentence)
        self.__words=[word for word in self.__stripped_sen]
