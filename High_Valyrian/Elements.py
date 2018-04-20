from Utils import *

class Word:

    def __init__(self,word, word_data):
         self.word=word
         self.meanings=word_data.get('meanings',[])
         self.synonyms=word_data.get('synonyms',[])
         self.sentences=word_data.get('sentences',[])
         self.length=len(word)
         self.__occurances=1

    def occured(self):
        self.__occurances+=1

    @property
    def complexity(self):
        return max((min((self.length*50 - self.__occurances),100),0))

    @property
    def needed_code(self):
        return 1*(len(self.meanings)==0)+2*(len(self.synonyms)==0)+4*(len(self.sentences)==0)

    def __str__(self):
        return self.word

class Sentence:

    def __init__(self, sentence):
        self.sentence=sentence
        self.__stripped_sen=strip_search(sentence)
        self.__words=[Word(word) for word in self.__stripped_sen]
        self.length=len(self.__words)

    @property
    def complexity(self):
        return sum([(word.complexity/self.length) for word in self.__words])
