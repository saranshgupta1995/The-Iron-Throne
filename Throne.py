from time import time, sleep
import threading
from random import randint
#Imports
#Team modules
from Council import call_council

global_l=threading.Lock()

Citidel,Mel,The_Language,Tkint,Davos,LittleFinger=call_council()

citidel=Citidel.Citidel()
mel=Mel.Mel()
language=The_Language.Valyrian()
face=Tkint.Face(citidel)
davos=Davos.Davos(citidel)
lf=LittleFinger.LittleFinger(citidel)


import os
from difflib import SequenceMatcher
import pyperclip

from Tkint.Utilities import send_input

print('imported everything')

#Running Mode
useSpeech=False
useUI=False
useVarys=True

def kill_and_raise(mod=None):
    global davos
    global citidel
    global mel
    global lf
    global face
    global language
    if(mod=='davos'):
        reload(Davos)
        davos= Davos.Davos(citidel)
    if(mod=='mel'):
        reload(Mel)
        mel=Mel.Mel()
    if(mod=='lang'):
        reload(The_Language)
        language=The_Language.Valyrian()
    if(mod=='lf'):
        reload(LittleFinger)
        lf=LittleFinger.LittleFinger(citidel)
    if(mod=='citidel'):
        citidel.loadData()
if(useVarys):
    def readCmd():
        with open('Citidel//Temp.txt','r') as f:
            while global_l.locked():
                continue
            global_l.acquire()
            cmd=f.read()[5:]
            global_l.release()
        return cmd

    def rawCmd():
        while global_l.locked():
            continue
        global_l.acquire()
        f=open(citidel.consts['temp_file_path'],"r")
        t=f.read()
        f.close()
        global_l.release()
        return t

    def fetchCmd(cmd):
        return citidel.cmds.get(cmd,cmd)

    def areSimilar(a,b):
        similar=SequenceMatcher(None, a, b).ratio()>0.8
        if(similar):
            while global_l.locked():
                continue
            global_l.acquire()
            with open('Citidel//Temp.txt','w') as f:
                f.write(str(randint(10000,99999))+b)
            global_l.release()
        return similar

    def getCmdData(cmd):
        face.cmdDet=True
        cmd=rawCmd()
        while(cmd==rawCmd()):
            continue
        cmd=readCmd()
        face.cmdDet=False
        return cmd

    def execCmd(action):
        print ('gonna exec', action)
        if(action=='raise'):
            citidel.info_data=citidel.consts['info_raise']
            mod=getCmdData(action)
            kill_and_raise(mod)
            citidel.info_data=citidel.consts['info_raise_s']
            return 1
        if(areSimilar("listen to the king",action)):
            citidel.info_data=citidel.consts['info_listen_king']
            return 1
        if(areSimilar("get me these lyrics",action)):
            song=pyperclip.paste()
            print(song)
            link=mel.getYoutubeBestSearch(song+" lyrics")
            print(song)
            mel.downloadAudioFrom(link)
            return 1
        if(areSimilar("get me this song",action)):
            print ('in getting song', action)
            song=getCmdData(action)
            print(song)
            if(song):
                link=mel.getYoutubeBestSearch(song)
                mel.downloadAudioFrom(link)
            return 1
        if(action[0] in ('+','-')):
            print('in block 1')
            details=getCmdData(action)
            print('got details')
            target=getCmdData(details)
            print(action,target,details)
            if('salary' in details.lower()):
                lf.add_salary(action,target)
                return 1
            lf.add_log(action, target, details)
            return 1
        elif(action[0] == '$'):
            action=action[1:]
            src=getCmdData('$'+action)
            print'src',src
            trgt=getCmdData(src)
            print 'trgt', trgt
            lf.do_transfer(action,src,trgt)
            return 1
        if(areSimilar("duck, find me this",action)):
            query=getCmdData(action)
            mel.get_info_on(query=query)
            return 1
        if(areSimilar("get the meaning of",action)):
            print 'enter word'
            word=getCmdData(action)
            print ('word lookup',word)
            word=language.get_word(word)
            data='\n'.join(word.meanings)
            citidel.info_data=data
            return 1
        if(areSimilar("get word data",action)):
            print 'enter word'
            word=getCmdData(action)
            print ('word lookup',word)
            word=language.get_word(word)
            print word.meanings
            print word.synonyms
            data_m='\n'.join(word.meanings)
            data_sy='\n'.join(word.synonyms)
            data_sn='\n'.join(word.sentences)
            citidel.info_data='It may mean any of the following.'
            sleep(0.1)
            citidel.info_data=data_m
            sleep(0.1)
            citidel.info_data='Do you need the synonyms? Enter more for more info.'
            need=getCmdData(word.word)
            print need
            if(need=='more'):
                print(need, data_sy)
                citidel.info_data=data_sy
                sleep(0.1)
                citidel.info_data='Do you need some example sentences? Enter more for more info.'
                need=getCmdData(need)
                if(need=='more'):
                    citidel.info_data=data_sn
            return 1
        if(areSimilar("duck, work secretly",action)):
            query=getCmdData(action)
            mel.get_info_on(query=query,incog=True)
            return 1
        if(areSimilar("goo, find me this",action)):
            query=getCmdData(action)
            mel.get_info_on(query=query,goo=True)
            return 1
        if(areSimilar("goo, work secretly",action)):
            query=getCmdData(action)
            mel.get_info_on(query=query,goo=True,incog=True)
            return 1
        if(areSimilar("calculate exp",action)):
            pyperclip.copy(mel.calculate_this(pyperclip.paste()))
            return 1
        return 0

def show_ui():
    while True:
        in_sen=face.take_Input()
        if(in_sen[0] in ('+','-','$')):
            send_input(in_sen)
            continue
        if(in_sen=="IS_CMD"):
            continue
        res=face.find_response(in_sen)
        print('response',res)
        if((res in citidel.cmds.values())):
            send_input(res)
            continue
        if(face.cmdDet):
            send_input(res)
            face.cmdDet=False
            continue
        face.respond_with(str(res))

if(citidel.useGamepad):
    def hook_gamepad():
        while True:
            citidel.check_gamepad()

print('show ui')

t=threading.Thread(target=show_ui)

t.start()

if(citidel.useGamepad):
    t1=threading.Thread(target=hook_gamepad)
    t1.start()

action_buff=rawCmd()
action=rawCmd()
while True:
    while(action==action_buff):
        try:
            action=rawCmd()
        except:
            print "Exception occured in main thread"
    cmd=readCmd()
    cmd=fetchCmd(cmd)
    execCmd(cmd)
    action_buff=rawCmd()
    action=rawCmd()
