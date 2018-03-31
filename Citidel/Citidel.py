
import json, os

class Citidel:

    def __init__(self):
        self.consts = json.loads(open('Citidel//consts.txt').read())
        self.cmds = json.loads(open('Citidel//cmds.txt').read())

    def getCmd(self):
        f=open((os.path.join(os.getcwd(),'Citidel','Temp.txt')),"r")
        t=f.read()
        f.close()
        return t
