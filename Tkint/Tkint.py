import Tkinter as Tk
import nltk, time, os
from random import choice
from Utilities import *

"""
CC: Coordinating Cunjunction
RB: Adverbs
IN: Preposition
NN: Noun
NNS: Plural Noun
JJ: Adjective
VBP: Verb
AT: Articl
VBD: Past tense verb
CD: Cardinal Number
DT: Determiner
"""

class Face:

    def __init__(self,citidel=None):
        if(not citidel):
            from Citidel.Citidel import Citidel
            citidel=Citidel()
        self.__citidel=citidel
        self.cmdDet=False
        self.__character='tyrion'
        self.__window=Tk.Tk()
        self.__window.title("The Iron Throne")
        self.__window.geometry("300x400")
        self.__labels=[]
        for i in range(15):
            self.add_label('')
        self.__textBox=Tk.Entry(self.__window)
        self.__textBox.pack()
        self.__buttons=[]
        self.__cmd=""
        print ('Face loaded')

##        lbl=Tk.Label(window,text="Label 1")
##        lbl.pack()
##        lbl1=Tk.Label(window,text="Label 21")
##        lbl1.pack()
##        ent=Tk.Entry(window)
##        ent.pack()
##        btn=Tk.Button(window,text="Btn")
##        btn.pack()

    def take_Input(self):
        self.__cmd=">"
        self.__textBox.delete(0,'end')
        while self.__cmd[-1]!="<":
            self.__cmd=">"+self.__textBox.get()
            self.__window.update_idletasks()
            self.__window.update()
        self.respond_with(self.__cmd[1:-1])
        if(self.__cmd[1:-1] in ('quit','exit')):
            self.removeUI()
        if(self.cmdDet):
            print ('sending input')
            send_input(self.__cmd[1:-1].lower())
            self.cmdDet=False
        return self.__cmd[1:-1].lower()

    def add_label(self,txt):
        self.__labels+=[Tk.Label(self.__window,text=txt)]
        self.__labels[len(self.__labels)-1].pack()

    def respond_with(self, txt=""):
        for i in range(len(self.__labels)-1):
            self.__labels[i]['text']=self.__labels[i+1]['text']
        self.__labels[len(self.__labels)-1]['text']=txt

    def removeUI(self):
        self.__window.destroy()

    def fetch_response(self,gist):
        reply=choice(self.__citidel.convs_out[gist])
        return reply

    def find_response(self,in_sen):
        means=[]
        meaning=find_meaning_in(in_sen,self.__citidel.convs_in,self.__citidel.convs_deep)
        if(meaning):
            return self.fetch_response(meaning)
        means+=[in_sen]
        while True:
            self.respond_with('What do you mean by that?')
            in_sen=self.take_Input()
            if(in_sen in ('nothing','ignore')):
                return 'As your Grace commands.'
            meaning=find_meaning_in(in_sen,self.__citidel.convs_in,self.__citidel.convs_deep)
            if(meaning):
                self.__citidel.convs_in[meaning]+=means
                self.__citidel.close_convs()
                self.__citidel.open_convs()
                return self.fetch_response(meaning)
            means+=[in_sen]
            if(len(means)>5):
                return 'I did not get you.'


if __name__=="__main__":
    d=Face()
    while True:
        res=str(d.take_Input())
        res=d.find_response(res)
        print(str(res))
        d.respond_with(str(res))
        print(str(res))
        d.respond_with(str(res))
    d.removeUI()
