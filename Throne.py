from time import time, sleep
import threading, os, pyperclip
from difflib import SequenceMatcher

## only used for randkey
from random import randint

## used to call council modules
from Council import call_council

global_l=threading.Lock()

## all loaded modules
Citidel, Mel, The_Language, Tkint, Davos, LittleFinger, Bran, Luwin = call_council()

##spawn council
citidel=Citidel.Citidel()
mel=Mel.Mel()
luwin=Luwin.Luwin(citidel)
language=The_Language.Valyrian()
face=Tkint.Face(citidel)
davos=Davos.Davos(citidel)
lf=LittleFinger.LittleFinger(citidel)
bran=Bran.Bran()

print('imported everything')

#Running Mode
useSpeech=False
useUI=False
useVarys=True

## reload modules for easier testing and development
## Simply reload module instead of restarting project
def kill_and_raise(mod=None):
    global davos
    global citidel
    global mel
    global lf
    global face
    global language
    global bran
    if(mod=='davos'):
        reload(Davos)
        davos= Davos.Davos(citidel)
    if(mod=='bran'):
        reload(Bran)
        bran= Bran.Bran()
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

def wait_for_lock():
    while global_l.locked():
        continue
    global_l.acquire()


## read cmd without randkey
def readCmd():
    wait_for_lock()
    with open('Citidel//Temp.txt','r') as f:
        cmd=f.read()[5:]
    global_l.release()
    return cmd

## read raw text from cmd file
def rawCmd():
    wait_for_lock()
    f=open(citidel.consts['temp_file_path'],"r")
    t=f.read()
    f.close()
    global_l.release()
    return t

def send_input(txt):
    wait_for_lock()
    with open('Citidel//Temp.txt','w') as f:
        f.write(str(randint(10000,99999))+txt)
    global_l.release()

## if cmd is sent via varys, fetch its meaning from citidel else return same cmd
def fetchCmd(cmd):
    return citidel.cmds.get(cmd,cmd)

## remove minor errors if present
## will be useful later
def areSimilar(a,b):
    return SequenceMatcher(None, a, b).ratio()>0.8

## get cmd data whenever needed
def getCmdData(cmd):
    face.cmdDet=True
    cmd=rawCmd()
    while(cmd==rawCmd()):
        continue
    cmd=readCmd()
    face.cmdDet=False
    return cmd

## execution function
def execCmd(action):
    try:
        print ('gonna exec', action)
        if(action=='raise'):
            luwin.new_event('raise')
            mod=getCmdData(action)
            luwin.in_event('raise',mod)
            kill_and_raise(mod)
            luwin.end_event()
            return 1
        if(areSimilar("listen to the king",action)):
            luwin.new_event('listen to the king')
            luwin.end_event()
            return 1
        if(areSimilar("get me these lyrics",action)):
            luwin.new_event('song lyrics download')
            song=pyperclip.paste()
            link=mel.getYoutubeBestSearch(song+" lyrics")
            luwin.in_event(song)
            download_thread=threading.Thread(target=mel.downloadAudioFrom, args=(link,))
            download_thread.start()
            luwin.end_event()
            return 1
        if(areSimilar("get me this song",action)):
            luwin.new_event('song name download')
            song=getCmdData(action)
            luwin.in_event(song)
            if(song):
                link=mel.getYoutubeBestSearch(song)
                download_thread=threading.Thread(target=mel.downloadAudioFrom, args=(link,))
                download_thread.start()
                luwin.in_event(song)
                luwin.end_event()
            return 1
        if(action[0] in ('+','-')):
            luwin.new_event('money log')
            details=getCmdData(action)
            luwin.in_event(action,details)
            target=getCmdData(details)
            luwin.in_event(action,details, target)
            if('salary' in details.lower()):
                lf.add_salary(action,target)
                return 1
            lf.add_log(action, target, details)
            luwin.end_event()
            return 1
        elif(action[0] == '$'):
            luwin.new_event('money transfer')
            action=action[1:]
            src=getCmdData('$'+action)
            luwin.in_event(action, src)
            trgt=getCmdData(src)
            luwin.in_event(action, src, trgt)
            lf.do_transfer(action,src,trgt)
            luwin.end_event()
            return 1
        if(areSimilar("duck, find me this",action)):
            luwin.new_event('ducky search')
            query=getCmdData(action)
            luwin.in_event(query)
            mel.get_info_on(query=query)
            luwin.end_event()
            return 1
        if(areSimilar("get the meaning of",action)):
            luwin.new_event('meaning fetch')
            word=getCmdData(action)
            luwin.in_event(word)
            word=language.get_word(word)
            data='\n'.join(word.meanings)
            ## TODO check for empty data
            citidel.info_data=data
            sleep(0.1)
            luwin.end_event()
            return 1
        if(areSimilar("tree mode",action)):
            luwin.new_event("tree mode")
            cmd=getCmdData(action)
            get_down=False
            path_list_needed=True
            path_list_refresh=True
            while(not get_down):
                if(areSimilar(cmd,'switch mode')):
                    get_down=True
                    continue
                if(path_list_needed):
                    trgt=cmd.lower()
                    bran.choose_tree(trgt)
                    pathList=bran.tree.all_leaves
                if(len(pathList) and path_list_refresh):
                    citidel.ui_scroller_data=pathList
                    citidel.ui_scroller=True
                cmd=getCmdData(action)
                path_list_refresh=True
                path_list_needed=True
                print cmd
                if(cmd[1:] in bran.tree.file_leaves or cmd[2:] in bran.tree.file_leaves):
                    path_list_refresh=False
                    path_list_needed=False
                    continue
                if(len(cmd)>1 and cmd[0]=='|' and cmd[1]!='.'):
                    if(bran.conflict):
                        bran.conflict=False
                        path_list_needed=False
                        bran.tree.tree=[branch for branch in cmd[1:].split('\\') if branch]
                        pathList=bran.tree.get_all_leaves()
                    else:
                        if(not cmd[1:] in bran.tree.file_leaves):
                            bran.tree.climb_up(cmd[1:])
                            pathList=bran.tree.get_all_leaves()
                            path_list_needed=False

                if(cmd[:2]=='>>'):
                    if(not cmd[2:] in bran.tree.file_leaves):
                        bran.get_inside(cmd[2:])
                        path_list_needed=False
                        path_list_refresh=False
                if(cmd[1:3]=='..'):
                    if(len(bran.tree.tree)>1):
                        bran.tree.move_down_branch()
                        pathList=bran.tree.get_all_leaves()
                    path_list_needed=False
            citidel.ui_scroller=True
            citidel.ui_scroller_data=[]
            sleep(0.2)
            luwin.end_event()

        if(areSimilar("open this",action)):
            luwin.new_event('open this')
            trgt=getCmdData(action)
            luwin.in_event(trgt)
            if(len(bran.show_glimpse(trgt))==1):
                bran.get_inside(bran.get_path(trgt))
            luwin.end_event()
        if(areSimilar("get word data",action)):
            luwin.new_event('word data')
            word=getCmdData(action)
            luwin.in_event(word)
            word=language.get_word(word)
            data_m='\n'.join(word.meanings)
            data_sy='\n'.join(word.synonyms)
            data_sn='\n'.join(word.sentences)
            citidel.info_data='It may mean any of the following.'
            sleep(0.1)
            citidel.info_data=data_m
            sleep(0.1)
            citidel.info_data='Do you need the synonyms? Enter more for more info.'
            need=getCmdData(word.word)
            if(need=='more'):
                citidel.info_data=data_sy
                sleep(0.1)
                citidel.info_data='Do you need some example sentences? Enter more for more info.'
                need=getCmdData(need)
                if(need=='more'):
                    citidel.info_data=data_sn
                    sleep(0.1)
            luwin.end_event()
            return 1
        if(areSimilar("duck, work secretly",action)):
            luwin.new_event('duck incog')
            query=getCmdData(action)
            luwin.in_event(query)
            mel.get_info_on(query=query,incog=True)
            luwin.end_event()
            return 1
        if(areSimilar("goo, find me this",action)):
            luwin.new_event('google this')
            query=getCmdData(action)
            luwin.in_event(query)
            mel.get_info_on(query=query,goo=True)
            luwin.end_event()
            return 1
        if(areSimilar("goo work secretly",action)):
            luwin.new_event('google incog')
            query=getCmdData(action)
            luwin.in_event(query)
            mel.get_info_on(query=query,goo=True,incog=True)
            luwin.end_event()
            return 1
        if(areSimilar("calculate exp",action)):
            luwin.new_event('calculating exp')
            pyperclip.copy(mel.calculate_this(pyperclip.paste()))
            luwin.end_event()b
            return 1
        return 0
    except Exception as e:
        luwin.log_err(e)
        sleep(0.1)

def show_ui():
    while True:
        in_sen=face.take_Input()
        if(in_sen in ('',"IS_CMD")):
            continue
        if(in_sen[0] in ('+','-','$')):
            send_input(in_sen)
            continue
        res=face.find_response(in_sen)
        if((res in citidel.cmds.values())):
            send_input(res)
            continue
        if(face.cmdDet):
            send_input(res)
            face.cmdDet=False
            continue
        face.respond_with(str(res))
        face.fake_typing()

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
