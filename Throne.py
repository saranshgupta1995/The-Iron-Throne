from time import time

a=time()

import threading, os

## only used for randkey
from random import randint

with open('Logger//Time_log.txt','a') as f:
    f.write('\nBasic Import 1 time log- '+str(time()-a))

a=time()
## used to call council modules
from Council import call_council

from throne_cmds import execCmd

with open('Logger//Time_log.txt','a') as f:
    f.write('\nBasic Import 2 time log- '+str(time()-a))

a=time()

Citidel, Mel, The_Language, Tkint, Davos, LittleFinger, Bran, Luwin = call_council()

with open('Logger//Time_log.txt','a') as f:
    f.write('\nCouncil Call time log- '+str(time()-a))

global_l=threading.Lock()

class Throne:

    def __init__(self):
        ## all loaded modules
        a=time()
        self.citidel=Citidel.Citidel()
        self.mel=Mel.Mel()
        self.luwin=Luwin.Luwin(self.citidel)
        self.language=The_Language.Valyrian(self.citidel)
        self.face=Tkint.Face(self.citidel)
        self.davos=Davos.Davos(self.citidel)
        self.lf=LittleFinger.LittleFinger(self.citidel)
        self.bran=Bran.Bran()
        with open('Logger//Time_log.txt','a') as f:
            f.write('\nObject Creation time log- '+str(time()-a))
        print('imported everything')
        t=threading.Thread(target=self.show_ui)
        t.start()
        if(self.citidel.useGamepad):
            t1=threading.Thread(target=self.hook_gamepad)
            t1.start()
        action_buff=self.rawCmd()
        action=self.rawCmd()
        while True:
            while(action==action_buff):
                try:
                    action=self.rawCmd()
                except:
                    print "Exception occured in main thread"
            cmd=self.readCmd()
            cmd=self.fetchCmd(cmd)
            execCmd(self.citidel, self.mel, self.language, self.face, self.davos, self.lf, self.bran, self.luwin, cmd, self.getCmdData, self.kill_and_raise)
            action_buff=self.rawCmd()
            action=self.rawCmd()


## reload modules for easier testing and development
## Simply reload module instead of restarting project
    def kill_and_raise(self,mod=None):
        if(mod=='davos'):
            reload(Davos)
            self.davos= Davos.Davos(self.citidel)
        if(mod=='bran'):
            reload(Bran)
            self.bran= Bran.Bran()
        if(mod=='mel'):
            reload(Mel)
            self.mel=Mel.Mel()
        if(mod=='lang'):
            reload(The_Language)
            self.language=The_Language.Valyrian(self.citidel)
        if(mod=='lf'):
            reload(LittleFinger)
            self.lf=LittleFinger.LittleFinger(self.citidel)
        if(mod=='citidel'):
            self.citidel.loadData()

    def wait_for_lock(self):
        while global_l.locked():
            continue
        global_l.acquire()


## read cmd without randkey
    def readCmd(self):
        self.wait_for_lock()
        with open('Citidel//Temp.txt','r') as f:
            cmd=f.read()[5:]
        global_l.release()
        return cmd

## read raw text from cmd file
    def rawCmd(self):
        self.wait_for_lock()
        f=open(self.citidel.consts['temp_file_path'],"r")
        t=f.read()
        f.close()
        global_l.release()
        return t

    def send_input(self,txt):
        self.wait_for_lock()
        with open('Citidel//Temp.txt','w') as f:
            f.write(str(randint(10000,99999))+txt)
        global_l.release()

## if cmd is sent via varys, fetch its meaning from citidel else return same cmd
    def fetchCmd(self,cmd):
        return self.citidel.cmds.get(cmd,cmd)

## get cmd data whenever needed
    def getCmdData(self,cmd):
        if(len(self.citidel.in_cmd_data)):
            cmd=self.citidel.in_cmd_data[0]
            self.citidel.in_cmd_data=self.citidel.in_cmd_data[1:]
            return cmd
        self.face.cmdDet=True
        cmd=self.rawCmd()
        while(cmd==self.rawCmd()):
            continue
        cmd=self.readCmd()
        self.face.cmdDet=False
        self.face.empty_header()
        return cmd

    def show_ui(self):
        while True:
            in_sen=self.face.take_Input()
            if(in_sen in ('',"IS_CMD")):
                continue
            if(in_sen[0] in ('+','-','$')):
                self.send_input(in_sen)
                continue
            res=self.face.find_response(in_sen)
            if((res in self.citidel.cmds.values())):
                self.send_input(res)
                continue
            if(self.face.cmdDet):
                self.send_input(res)
                self.face.cmdDet=False
                continue
            self.face.respond_with(str(res))
            self.face.fake_typing()

    def hook_gamepad(self):
        while True:
            self.citidel.check_gamepad()



throne=Throne()
