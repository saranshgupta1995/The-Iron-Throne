import json
from time import sleep

from datetime import datetime as dt

class Luwin:

    def __init__(self, citidel):
        self.__log=[]
        self.__citidel=citidel
        self.__event=''
        self.__wisdom = json.loads(open('Luwin//Wisdom.json').read())

    def new_event(self,e):
        self.__event=e
        self.__log=['\n'+e + " set to occur."]
        self.say_stuff()

    def say_stuff(self):
        self.__citidel.info_data=self.__wisdom[self.__event][len(self.__log)-1]
        sleep(0.1)

    def in_event(self, *data):
        self.__log+=[self.__event + " occured with data [" +", ".join(data)+'] at '+str(dt.now())+'.']
        self.say_stuff()

    def end_event(self):
        self.__citidel.info_data='Winter is coming your grace. Time is a matter o concern, now, more than ever.'
        with open('Luwin_Log.txt','a') as f:
            f.write('\n'.join(self.__log)+'\n'+self.__event+' successfully completed\n')
        sleep(0.1)

    def log_err(self, err):
        with open('Luwin_Log.txt','a') as f:
            f.write('\n'.join(self.__log) + '\n\tError found: '+str(err))
        self.__log=[]
        self.__citidel.info_data="An Error Occured. Please try again. Luwin Logs have error details."
