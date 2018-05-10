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

class Scroller:

    def __init__(self,data):
        self.__data=data
        self.choice=0
        self.__i=0
        self.__j=15
        self.window_data=self.__data[self.__i:self.__j]

    def scroll_down(self):
        will_change=(self.__j<len(self.__data)) and self.choice==14
        self.__i+=1*will_change
        self.__j+=1*will_change
        self.window_data=self.__data[self.__i:self.__j]
        if(not will_change):
            self.choice=min((len(self.__data)-1,14,self.choice+1))
        return (will_change)

    def scroll_up(self):
        will_change=self.choice==0 and self.__i>0
        self.__i-=1*will_change
        self.__j-=1*will_change
        self.window_data=self.__data[self.__i:self.__j]
        if(not will_change):
            self.choice=max((0,self.choice-1))
        return (will_change)

class Face:

    def __init__(self,citidel=None):
        if(not citidel):
            from Citidel.Citidel import Citidel
            citidel=Citidel()
        self.__citidel=citidel
        self.cmdDet=False
        self.__scroller=None
        self.__character='tyrion'
        self.__window=Tk.Tk()
        self.__window.title("The Iron Throne")
        self.__window.geometry("300x500")
        Tk.Label(self.__window,text='',width=36,wraplength=250).pack()
        self.__textBox=Tk.Entry(self.__window)
        self.__textBox.bind("<KeyPress>",self.key_down)
        self.__textBox.pack()
        Tk.Label(self.__window,text='',width=36,wraplength=250).pack()
        self.__labels=[]
        for i in range(15):
            self.add_label('')
        self.__buttons=[]
        self.__cmd=""
        with open(r'C:\Users\Saransh\Dropbox\Temps\Throne Cmds.txt','r') as fp:
            self.__drpbx_cmds=fp.read().split('\n')
        print ('Face loaded')

    def scroll_up(self):
        action=self.__scroller.scroll_up()
        if(action):
            self.respond_with(self.__scroller.window_data[0])
        self.__labels[self.__scroller.choice]['bg']='white'
        self.__labels[self.__scroller.choice+1]['bg']='SystemButtonFace'

    def scroll_down(self):
        action=self.__scroller.scroll_down()
        if(action):
            self.respond_with(self.__scroller.window_data[-1], norm=False)
        self.__labels[self.__scroller.choice]['bg']='white'
        self.__labels[self.__scroller.choice-1]['bg']='SystemButtonFace'

    def dive_into(self, target):
        send_input('|'+target)

    def move_out(self, target):
        send_input('|..'+target)

    def target_found(self):
        send_input('>>' +self.__labels[self.__scroller.choice]['text'])

    def key_down(self,event):
        if(self.__scroller):
            if(event.keycode==38):
                self.scroll_up()
            elif(event.keycode==40):
                self.scroll_down()
            elif(event.keycode==39):
                self.dive_into(self.__labels[self.__scroller.choice]['text'])
            elif(event.keycode==37):
                self.move_out(self.__labels[self.__scroller.choice]['text'])
            elif(event.keycode==13):
                self.target_found()

    def take_Input(self):
        self.__textBox.focus()
        self.__cmd=">"
        self.__textBox.delete(0,'end')
        while self.__cmd[-1]!="<":
            if(len(self.__citidel.info_data)):
                self.respond_with(self.__citidel.info_data)
                self.__citidel.info_data=''
            if(len(self.__citidel.ui_scroller_data) and self.__citidel.ui_scroller):
                self.__citidel.ui_scroller=False
                self.enter_scroller(self.__citidel.ui_scroller_data)
            if((not len(self.__citidel.ui_scroller_data)) and self.__citidel.ui_scroller):
                self.__citidel.ui_scroller=False
                self.exit_scroller()
            self.__cmd=">"+self.__textBox.get()
            self.__window.update_idletasks()
            self.__window.update()
        self.__textBox.delete(0,'end')
        self.__window.update_idletasks()
        self.__window.update()
        if(self.__cmd[1:-1]=='done with scroller'):
            self.exit_scroller()
        if(self.__cmd[1:-1]=='sync pending'):
            self.__cmd='>'+self.__drpbx_cmds[0]+'<'
            self.__drpbx_cmds=self.__drpbx_cmds[1:]
        if(self.__cmd[1:-1]==''):
            return ''
        self.respond_with(self.__cmd[1:-1],'e')
        in_sen=strip_search(self.__cmd[1:-1])
        if(in_sen in ('quit','exit')):
            print 'exiting by exit'
            self.removeUI()
        if(self.cmdDet):
            print ('sending input')
            send_input(in_sen)
            self.cmdDet=False
            return "IS_CMD"
        in_sen,self.__citidel.in_cmd_data=check_for_data(in_sen)
        return in_sen.lower()

    def add_label(self,txt):
        self.__labels+=[Tk.Label(self.__window,text=txt,width=36,wraplength=250,font=("verdana", 9))]
        self.__labels[len(self.__labels)-1].pack()

    def respond_with(self, txt="", anc='w',norm=True):
        if(norm):
            for i in range(len(self.__labels)-1,0,-1 ):
                self.__labels[i]['text']=self.__labels[i-1]['text']
                self.__labels[i]['anchor']=self.__labels[i-1]['anchor']
                self.__labels[i]['justify']=self.__labels[i-1]['justify']
            self.__labels[0]['text']=txt
            self.__labels[0]['anchor']=anc
            self.__labels[0]['justify']=(['left','right'][anc=='e'])
        else:
            for i in range(0,len(self.__labels)-1):
                self.__labels[i]['text']=self.__labels[i+1]['text']
                self.__labels[i]['anchor']=self.__labels[i+1]['anchor']
                self.__labels[i]['justify']=self.__labels[i+1]['justify']
            self.__labels[-1]['text']=txt
            self.__labels[-1]['anchor']=anc
            self.__labels[-1]['justify']=(['left','right'][anc=='e'])


    def removeUI(self):
        self.__window.destroy()

    def enter_scroller(self, data):
        self.__temp_labels=[(label['text'],label['anchor']) for label in self.__labels]
        self.__scroller=Scroller(data)
        for i in range(15):
            self.__labels[i]['text']=''
            self.__labels[i]['bg']=['SystemButtonFace','white'][self.__scroller.choice==i]
        for i in range(min([len(data),15]),0,-1):
            self.respond_with(data[i-1])

    def exit_scroller(self):
        self.__scroller=None
        for i in range(15):
            self.respond_with(self.__temp_labels[i][0],self.__temp_labels[i][1])
            self.__labels[i]['bg']='SystemButtonFace'

    def fetch_response(self,gist):
        reply=choice(self.__citidel.convs_out[gist])
        return reply

    def fake_typing(self):
        a=time.time()
        top_label=(self.__labels[0]['text'],self.__labels[0]['anchor'])
        self.__labels[0]['anchor']="w"
        self.__labels[0]['justify']="left"
        wait_period=max(int(len(top_label[0])/30),0.5)
        while(time.time()-a<wait_period):
            time_passed=((time.time()-a)*100)/wait_period
            to_write=int(time_passed*len(top_label[0])/100)
            self.__labels[0]['text']=top_label[0][:to_write]
            self.__window.update_idletasks()
            self.__window.update()
        self.__labels[0]['text']=top_label[0]
        self.__labels[0]['anchor']=top_label[1]
        self.__labels[0]['justify']=(['left','right'][top_label[1]=='e'])

    def find_response(self,in_sen):
        means=[]
        meaning=find_meaning_in(in_sen,self.__citidel.convs_in,self.__citidel.convs_deep)
        if(not len(meaning)):
            meaning=find_meaning_in(strip_search(in_sen,self.__citidel.stop_words),self.__citidel.convs_in,self.__citidel.convs_deep)
        if(meaning):
            return self.fetch_response(meaning)
        means+=[in_sen]
        while True:
            self.respond_with('What do you mean by that?')
            in_sen=self.take_Input()
            if(in_sen in ('nothing','ignore')):
                return 'As your Grace commands.'
            meaning=find_meaning_in(in_sen,self.__citidel.convs_in,self.__citidel.convs_deep)
            if(not len(meaning)):
                meaning=find_meaning_in(strip_search(in_sen,self.__citidel.stop_words),self.__citidel.convs_in,self.__citidel.convs_deep)

            if(meaning):
                self.__citidel.convs_in[meaning]+=means
                self.__citidel.close_convs()
                self.__citidel.open_convs()
                return self.fetch_response(meaning)
            means+=[in_sen]
            if(len(means)>5):
                return 'I did not get you.'
