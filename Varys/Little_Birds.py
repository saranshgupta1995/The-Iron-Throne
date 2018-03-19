import os,pickle
from difflib import SequenceMatcher
import random

grph={}

drives=["F"]


bsname=os.path.basename
orig_path=os.getcwd()

def addtogrph(branch,node):
    if node in list(grph.keys()):
        grph[node]=grph[node]+[branch]
    else:
        grph[node]=[branch]
    if(random.randint(1,1000)<6):
        print(node,branch)

def addtogrph2(branch,node):
    grph[node]=grph.get(node,[])+[branch]

def readfoldersin(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def readfilesin(path):
    return [d for d in os.listdir(path) if not os.path.isdir(os.path.join(path, d))]

def iterthrough(path):
    os.chdir(path)
    if(len(readfilesin(path))<1000):
        for filee in readfilesin(path):
            if not filee.startswith('.'):
                addtogrph(path,filee)
    for folder in readfoldersin(path):
        addtogrph(path,folder)
        newpath=path+"\\"+folder
        if(os.path.isdir(newpath)):
            if not folder.startswith('.'):
                try:
                    os.chdir(newpath)
                    iterthrough(newpath)
                except:
                    pass

def findpath(dest):
    poss=[]
    for value in grph.values():
        try:
            value.index(dest)
            poss.append(list(grph.keys())[list(grph.values()).index(value)])
        except :
            pass
    return poss

if(not os.path.exists("datadict1.p")):
    print("run")
    for drive in drives:
        drivepath=drive+":\\"
        iterthrough(drivepath)
        os.chdir(orig_path)
    pickle.dump(grph,open("datadict.p","wb"))
