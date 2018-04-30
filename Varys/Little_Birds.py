import os,pickle
import random

class Little_Bird:

    def __init__(self):
        self.data={}
        self.surveyed={}
        self.drives=['F:\\']
        self.orig_path=os.getcwd()
        self.filtered_folders=['node_modules','$RECYCLE.BIN']
        self.mode='collect'

    def add_data(self,parent, child):
        parent=parent.lower()
        child=child.lower()
        if(self.mode=='collect'):
            self.data[child]=self.data.get(child,[])+[parent]
        elif(self.mode=='new_survey'):
            if(parent not in self.data.get(child,[])):
                self.surveyed[child]=self.surveyed.get(child,[])+[parent]


    def get_folders(self,path):
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    def get_files(self,path):
        return [d for d in os.listdir(path) if not os.path.isdir(os.path.join(path, d))]

    def get_data(self,path):
        if(len(self.get_files(path))<1000):
            [self.add_data(path, f) for f in self.get_files(path) if not f.startswith('.')]
        for folder in self.get_folders(path):
            if not folder.startswith('.'):
                if not folder in self.filtered_folders:
                    self.add_data(path, folder)
                    new_path=os.path.join(path, folder)
                    if(os.path.isdir(new_path)):
                        try:
                            self.get_data(new_path)
                        except:
                            print 'failed to capture data for '+folder

    def new_survey(self):
        self.surveyed={}
        self.mode='new_survey'
        x=open("datadict.p","rb")
        self.data = pickle.load(x)
        x.close()
        self.fly()
        return [value+'\\'+key for key in self.surveyed.keys() for value in self.surveyed[key]]

    @property
    def survey_len(self):
        return sum([len(x) for x in self.surveyed.values()])

    def remember_data(self):
        os.chdir(self.orig_path)
        pickle.dump(self.data,open("datadict.p","wb"))

    def capture_data(self):
        self.mode='collect'
        self.fly()
        self.remember_data()

    def fly(self):
        for drive in self.drives:
            self.get_data(drive)
