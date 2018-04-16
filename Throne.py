from time import time
import threading
#Imports
#Team modules

start_time=time()

wait_Tkint=0
def get_Tkint():
    a=time()
    global wait_Tkint
    from Tkint import Tkint
    wait_Tkint=Tkint
    with open('Logger//Time_log.txt','a') as f:
        f.write('\nTkint time log- '+str(time()-a))
getting_Tkint=threading.Thread(target=get_Tkint)
getting_Tkint.start()
wait_Citidel=0
def get_Citidel():
    a=time()
    global wait_Citidel
    from Citidel import Citidel
    wait_Citidel=Citidel
    with open('Logger//Time_log.txt','a') as f:
        f.write('\nCitidel time log- '+str(time()-a))
getting_Citidel=threading.Thread(target=get_Citidel)
getting_Citidel.start()
wait_Davos=0
def get_Davos():
    a=time()
    global wait_Davos
    from Davos import Davos
    wait_Davos=Davos
    with open('Logger//Time_log.txt','a') as f:
        f.write('\nDavos time log- '+str(time()-a))
getting_Davos=threading.Thread(target=get_Davos)
getting_Davos.start()
wait_Mel=0
def get_Mel():
    a=time()
    global wait_Mel
    from Mel import Mel
    wait_Mel=Mel
    with open('Logger//Time_log.txt','a') as f:
        f.write('\nMel time log- '+str(time()-a))
getting_Mel=threading.Thread(target=get_Mel)
getting_Mel.start()
wait_LF=0
def get_LF():
    a=time()
    global wait_LF
    from LittleFinger import LittleFinger
    wait_LF=LittleFinger
    with open('Logger//Time_log.txt','a') as f:
        f.write('\nLittleFinger time log- '+str(time()-a))
getting_LF=threading.Thread(target=get_LF)
getting_LF.start()

getting_Citidel.join()
Citidel=wait_Citidel
citidel=Citidel.Citidel()
getting_Mel.join()
Mel=wait_Mel
mel=Mel.Mel()
getting_Tkint.join()
Tkint=wait_Tkint
face=Tkint.Face(citidel)
getting_Davos.join()
Davos=wait_Davos
davos=Davos.Davos(citidel)
getting_LF.join()
LittleFinger=wait_LF
lf=LittleFinger.LittleFinger(citidel)


import os
from difflib import SequenceMatcher
import pyperclip

from Tkint.Utilities import send_input

with open('Logger//Time_log.txt','a') as f:
    f.write('\nTotal time log- '+str(time()-start_time)+'\n\n\n')


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
    if(mod=='davos'):
        reload(Davos)
        davos= Davos.Davos(citidel)
    if(mod=='mel'):
        reload(Mel)
        mel=Mel.Mel()
    if(mod=='lf'):
        reload(LittleFinger)
        lf=LittleFinger.LittleFinger(citidel)
    if(mod=='citidel'):
        citidel.loadData()
if(useVarys):
    def readCmd():
        return citidel.getCmd()

    def areSimilar(a,b):
        similar=SequenceMatcher(None, a, b).ratio()>0.8
        if(similar):
            with open('Citidel//Temp.txt','w') as f:
                f.write(b)
        return similar

    def fetchCmd():
        return citidel.cmds.get(readCmd(),readCmd())

    def getCmdData(cmd):
        face.cmdDet=True
        while(cmd==readCmd()):
            continue
        cmd=readCmd()
        face.cmdDet=False
        return cmd

    def execCmd(action):
        if(action=='raise'):
            mod=getCmdData(action)
            kill_and_raise(mod)
            return 1
        if(areSimilar("listen to the king",action)):
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
        if((res in citidel.cmds.values()) or face.cmdDet):
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

action_buff=fetchCmd()
action=fetchCmd()
while True:
    while(action==action_buff):
        action=fetchCmd()
    with open('Citidel//Temp.txt','r') as f:
        action=f.read()
    action_buff=action
    execCmd(action)
    action_buff=fetchCmd()
    action=fetchCmd()
